from flask import Flask ,render_template, request,redirect,session,make_response,json, url_for
from model import User
from smtpserver import EmailVerification

from db import MongoDB as mymongo
from my_jwtoken import JWT_Token
from bson.objectid import ObjectId
from speech2text import text2speech
import openai
from google.cloud import texttospeech_v1
from botfriend import BotFriend
from botfriendpreminium import BotFriendPreminium
from form_validate import form



mongodb_url="mongodb://localhost:27017"
premium_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiPGJvdW5kIG1ldGhvZCBPYmplY3RJZC5fX2hhc2hfXyBvZiBPYmplY3RJZCgnNjQzYjYyOGM5NzNjZGU2MTU3N2FkZjQxJyk-IiwiZmlyc3RfbmFtZSI6ImRlbmVtZSIsImxhc3RfbmFtZSI6ImRlbmVtZSIsImVtYWlsIjoiZGVuZW1lQGdtYWlsLmNvbSIsImV4cCI6MTY4MjIxODI1Mn0.EBCvXsgZ99lnR_zXBcl-f0wTdb2wBarxRapK70uH5mI"



app = Flask(__name__)


@app.route("/")
def home():  
    token = request.cookies.get('token')
    if token:
        tkn = JWT_Token()
        user = tkn.decode_token(token=token)      
        if type(user) == dict :
            name = user["first_name"] + " " + user["last_name"]
            return render_template("index.html" , name=name)
        else:
            return redirect("/login",302) 
    return render_template("index.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        m = mymongo(db_name="BOTFRIEND",url=mongodb_url)
        email = request.form["email"]
        password = request.form["password"]
        email = email.strip()
        password = password.strip()
        
        # veri tabanı için sorgu parametresi
        query = {'email': email}
        foundUser = m.find_one(collection_name="users", query=query)

        if foundUser is None:
            error = "kullanıcı adı veya şifre hatalı"
            return render_template("login.html", error=error)

        if foundUser["password"]== password:
            resp = make_response(redirect("/", 302))
            resp.set_cookie('token', foundUser["token"], httponly=True, secure=True)  # Güvenli çerez ayarları
            return resp

        error = "kullanıcı adı veya şifre hatalı"
        return render_template("login.html", error=error)

    return render_template("login.html")
 



@app.route("/signup",methods=["GET","POST"])
def signup():
    if request.method=='POST':
        m = mymongo(db_name="BOTFRIEND",url=mongodb_url)  
        
        formcontrol = form()
        
        email =  request.form['email'].strip()
        password = request.form['password'].strip()
        first_name = request.form['first_name'].strip()
        last_name = request.form['last_name'].strip()        
  
        bool_password = formcontrol.password_control(password = password)
        if not bool_password:
            error= "şifreniz en az 1 büyük harf 1 küçük harf ve 8 karakter uzunluğunda olmalıdır"
            return render_template("signup.html",error = error)  
        
        bool_email = formcontrol.validate_input(email)
        if not bool_email:
            error = "lütfen geçerli karakterleri giriniz"
            return render_template("signup.html",error = error)       
                 
        query={"email":email}
        
        userBool = m.find_one("users",query=query)
        if userBool!=None:
            error = "Bu email zaten mevcut"
            return render_template("signup.html",error = error)       

        mailBool =m.find_one("mail",query=query)
        if mailBool!=None:
            code = send_code_mail(email=email)
            data = {"code":code}
            m.update_one(collection_name="mail",query=query,data=data)
            resp = make_response(redirect("/verify", 302))
            resp.set_cookie('email', email, httponly=True, secure=True)  # Güvenli çerez ayarları
            return resp
        else:     
            code = send_code_mail(email=email)
            ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
            data = {"email":email,"first_name":first_name,"last_name":last_name,"password":password,"code":code,"addr":ip_address,"try":0}
            m.insert_one("mail",data=data)
            m.client.close()
            resp = make_response(redirect("/verify", 302))
            resp.set_cookie('email', email, httponly=True, secure=True)  # Güvenli çerez ayarları
            return resp
    else:
        return render_template("signup.html")


# Doğrulama sayfası
@app.route('/verify', methods=['GET', 'POST'])
def verify():
    m = mymongo(db_name="BOTFRIEND",url=mongodb_url) 
    email = request.cookies.get('email')

# POST isteği olduğunda doğrulama kodunu kontrol ediyoruz
    if request.method == 'POST':
        query={"email":email}
        ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
        user_verify = m.find_one(collection_name="mail",query=query)
        if ip_address != user_verify['addr']:
            return 'işlemnizin şuan gerçekleştirilemiyor daha sonra tekara deneyin'
        user_code = request.form['code']
        # Kullanıcının girdiği doğrulama kodu doğruysa, kullanıcının bilgilerini kaydediyoruz
        if user_code == user_verify[ 'code'] and int(user_verify['try']) < 4 :
            inserDatabese(first_name=user_verify["first_name"],last_name=user_verify["last_name"],email=user_verify["email"],password=user_verify["password"])
            # Kullanıcı doğrulandıktan sonra ana sayfaya yönlendiriyoruz
            resp = make_response(redirect(url_for('home')))
            resp.delete_cookie('email')
            user = m.find_one(collection_name="users",query=query)
            m.delete_one(collection_name="mail",query=query)
            resp.set_cookie("token",user["token"])
            return resp
        else:
            user_verify["try"]+=1
            return render_template('verify.html', error='Doğrulama kodu yanlış')
    m.client.close
    # GET isteği olduğunda doğrulama formunu gösteriyoruz
    return render_template('verify.html')


def send_code_mail(email):
    ev = EmailVerification(email_reciver=email)
    return ev.code
    
    
    
@app.route('/chat', methods=['POST','GET'])
def send_message():
    tokenh = JWT_Token()
    global usr
    if request.method=="POST":
        token = request.cookies.get('token')
        if token == None:
            return redirect("/login",302)

        user = tokenh.decode_token(token=token)
        
        
        client = texttospeech_v1.TextToSpeechClient()
        
        data = request.get_json()
        a = data['message']

        response = usr.api_query(a)

        email=user["email"]

        text2speech(client=client , userid=email ,input=response)  
        
        # Return the response to the frontend
        audio_path = "static/" + user["email"] + "/audio.mp3"
        return json.dumps({"audio_path": audio_path, "responseq": response})
    else:
        token = request.cookies.get('token')

        if token == None:
            return redirect("/login",302)
        user = tokenh.decode_token(token=token)

        if type(user) != dict :
            resp = make_response(redirect(url_for('login')))
            resp.delete_cookie('token')
            return 
        
        name = user[ 'first_name' ] + " " + user[ 'last_name' ]
        
        if token == premium_token:
            usr = BotFriendPreminium()
            return render_template("promt.html", name = name)
        else:
            usr = BotFriend()

        return render_template("chat.html", name = name )


@app.route("/logout")
def log_out():
    resp = make_response(redirect(url_for('login')))
    resp.delete_cookie('token')
    return resp


def inserDatabese(first_name,last_name,email,password):
        m = mymongo(db_name="BOTFRIEND",url=mongodb_url)  
        
        token = JWT_Token()
           
        uid = ObjectId()
        auth = "VISITED"
        
        userid= str(uid.__hash__)
        my_token = token.generate_token(first_name=first_name,last_name=last_name,email=email,userid=userid)
        
        usermodel = User(uid=uid ,user_id=userid,first_name=first_name,auth=auth,last_name=last_name,email=email,password=password,token=my_token).__dict__
        m.insert_one("users",data=usermodel)
        m.client.close
     
     
@app.route("/updatepromt", methods=["POST"])
def promt():
    if request.method=="POST":
        token = request.cookies.get('token')
        tokenh = JWT_Token()
        premium = BotFriendPreminium()
        if token == None:
            return redirect("/login",302)
        promt = request.form.get("promt").strip()
        print("yeni promt ",promt)
        
        premium.add_prompt(text=promt)
        return redirect("/chat",302)
    
@app.route("/updatepassword",methods=["GET","POST"])
def update_password():
    
    token = request.cookies.get('token')
    tokenh = JWT_Token()
    if token == None:
        return redirect("/login",302)

    user_datails = tokenh.decode_token(token=token)
    if type(user_datails)!=dict:
        return redirect("/login",302)
    
    passowrd = request.form.get("password")
    new_passowrd = request.form.get("newpassowrd")
    confirm_new_passowrd = request.form.get("confirmnewpassowrd")
    
    m = mymongo(db_name="BOTFRIEND",url=mongodb_url)  
    user = m.find_one(collection_name="users",query={"email":user_datails['email']})
    
    if passowrd!=user["password"]:
        error = "şifreniz hatalı"
        return render_template("x.html",error = error)

    if new_passowrd != confirm_new_passowrd :
        error = "şifreler uyuşmuyor"
        return render_template("x.html",error = error)

    
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8080, debug=True)
    
    
    
