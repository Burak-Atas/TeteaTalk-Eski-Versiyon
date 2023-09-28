import re

class form():
    #şifre uzunluğu ve en az bir büyük harf bir küçük harf kontrolü
    def password_control(self , password):
        if len(password) < 8:
           return False
    
        has_uppercase = False
        has_lowercase = False
        
        for char in password:
            if char.isupper():
                has_uppercase = True
            elif char.islower():
                has_lowercase = True
                
        if has_uppercase and has_lowercase:
            return True
        else:
            return False
    
    def validate_input(self,input_string):
        # Kullanıcı girişindeki yasaklı karakterleri filtrele
        sanitized_input = re.sub(r"[;\"'=%#(){}<>]", "", input_string)
        
        # Girilen değerin özelliklerine göre doğrulama yap
        if len(sanitized_input) < 3 or len(sanitized_input) > 50:
            return False
        if not re.match(r"^[a-zA-Z0-9_@.]*$", sanitized_input):
            return False

        
        # Tüm doğrulamaları geçerse True döndür
        return True
    
