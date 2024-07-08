import modals.connect as connect
from flask import Blueprint

admin = Blueprint("admin",__name__)

def login(username,password):
    cursor = connect.connect()
    cursor.execute('SELECT * from users where username=%s and password=%s',(username,password,))
    user= cursor.fetchone()
    if(user):
        return user
    else:
        print("there is no user named",username)
        return False