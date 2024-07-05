from flask import  Flask,redirect,url_for,render_template,request,jsonify
import modals.connect as db
import modals.admin as admin
import jwt

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def root():
    username = request.get_json()
    cursor = admin.login(username,password)
    user = jsonify(cursor)
    print(user)
    return user
    
        
if __name__ == '__main__':
    app.run(debug=True) 