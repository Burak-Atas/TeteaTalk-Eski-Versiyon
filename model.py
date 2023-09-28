from datetime import datetime, timedelta


class User:
    def __init__(self, uid, user_id, first_name, last_name, email, auth ,password, token):
        self.name = first_name
        self.last_name = last_name
        self.token = token 
        self.uid = uid 
        self.user_id = user_id
        self.email = email
        self.password = password
        self.auth = auth
        self.created_time= datetime.utcnow()

