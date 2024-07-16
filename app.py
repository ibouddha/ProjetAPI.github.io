from flask import  Flask,redirect,url_for,render_template,request,jsonify,json,session
import modals.connect as db
import admin.admin as admin
import users.users as users
import admin.admin as admin
import modals.functions as func
import jwt
import secrets

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_urlsafe(32)

app.register_blueprint(admin.admin_bp,url_prefix='/admin')
app.register_blueprint(users.user_bp,url_prefix='/users')

@app.route('/',methods=['GET','POST'])
def root():
    if(not func.auth):
        return ()
    
    username = session["username"]
    payload = {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60) # Token expires in 1 hour
        }
    token = jwt.encode(payload,app.config['SECRET_KEY'],algorithm = 'HS256')
    session['token'] = token
    return jsonify({'token':token})
    
        
if __name__ == '__main__':
    app.run(debug=True) 