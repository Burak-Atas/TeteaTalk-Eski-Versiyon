import os
import jwt
from datetime import datetime, timedelta

class JWT_Token():

    
    def generate_token(self, first_name, last_name, email, userid):
        # Token'ın son kullanma tarihi (1 saat sonrası)
        expiration = datetime.utcnow() + timedelta(weeks=1)
                
        # Token imzalama anahtarı
        secret_key = "hello"
        # Token imzalama algoritması
        algorithm = 'HS256'
        
        # Token oluşturma
        token = jwt.encode({'user_id': userid, 'first_name': first_name, 'last_name': last_name, 'email': email, 'exp': expiration}, secret_key, algorithm=algorithm)

        # Oluşturulan token'ı yazdırma
        return token
    
    def decode_token(self,token):

        # Token imzalama anahtarı
        secret_key = 'hello'

        # Token imzalama algoritması
        algorithm = 'HS256'

        # Token çözme
        try:
            decoded_token = jwt.decode(token, secret_key, algorithms=[algorithm])
            return decoded_token
        except jwt.ExpiredSignatureError:
            print('Token has expired')
        except jwt.InvalidSignatureError:
            print('Token has invalid signature')
        except jwt.DecodeError:
            print('Error decoding token')

        

if __name__=="__main__":
    jt = JWT_Token()
    x=jt.generate_token( "bural","atas","mahmut@gmail.com","1233")
    print(x)
