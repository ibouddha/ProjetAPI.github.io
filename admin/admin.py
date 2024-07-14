import modals.connect as connect
import modals.functions as func
from flask import Flask,Blueprint,request,json,session,jsonify
import datetime
import jwt

admin_bp = Blueprint("admin",__name__)

@admin_bp.route('/findAll',methods=["POST","GET"])
def getAllUsers():
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * from users')
    user= cursor.fetchall()
    if(len(user)):
        return user
    else:
        print("there is no user")
        return False
    
@admin_bp.route("/update/<string:username>",methods=["GET","POST"])
def getUserByUsername(username):
    newuser = request.get_json()
    user = func.getUser(username)
    if(user['user']!="404 no User with this name"):
        user['user']['email'] = newuser['email']
        user['user']['password'] = newuser['password']
        user['user']['groupe_id'] = newuser['groupe_id']
        user['user']['role'] = newuser['role']
        func.updateuser(user['user'])
    return user['user']
        

@admin_bp.route('/register',methods=["GET","POST"])
def register():
    data = request.get_json()
    conn = connect.connect()
    cursor = conn.cursor()
    # print(data["username"])
    cursor.execute('INSERT INTO users (user_id,username,password,email,id_groupe,role) VALUES (%s,%s,%s,%s,%s,%s)',(data['user_id'],data['username'],data['password'],data['email'],data['id_groupe'],data['role']))
    conn.commit()
    
@admin_bp.route('/add_user',methods=["POST","GET"])
def add_user():
    data = request.get_json()
    conn = connect.connect()
    cursor = conn.cursor()
    id_auto = func.count()[0]
    data['user_id']=id_auto+1
    cursor.execute('INSERT INTO users (user_id,username,password,email,id_groupe,role) values (%s,%s,%s,%s,%s,%s)',(data['user_id'],data['username'],data['password'],data['email'],data['id_groupe'],data['role']))
    conn.commit()
    conn.close()
    return {"id":id_auto}
    
@admin_bp.route('/',methods=['GET','POST'])
def index():
    return (f"Welcome {func.auth()}")
    