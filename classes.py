from validate import *


class Trip:
    def __init__(self,cost,start_time,end_time,status = "pending"):
        self.cost = cost
        self.start_time = start_time
        self.end_time = end_time
        self.status = status

class User:
    def __init__(self,username,password,user_type = "default_user"):
        self.username = validate_username(username)
        self.password = validate_password(password)
        self.user_type = user_type

class Dashboard:
    def __init__(self,user:User,wallet):
        self.user = user
        self.__wallet = wallet

    @property
    def wallet(self):
        return self.__wallet