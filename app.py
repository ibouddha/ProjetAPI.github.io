from flask import  Flask,redirect,url_for,render_template,request,jsonify,json
import modals.connect as db
import modals.admin as admin
import jwt
import secrets
import datetime

app = Flask(__name__)

app.config['SECRET_KEY'] = secrets.token_urlsafe(32)

@app.route('/',methods=['GET','POST'])
def root():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if not username or not password:
            return jsonify({'error': 'Missing username or password'}), 400
    
    cursor = admin.login(username,password)
    if not cursor:
        return jsonify({'error': 'Invalid username or password'}), 400
    
    datum = {'id':cursor[0],'username':cursor[1],'password' : cursor[2],'email':cursor[3],'groupeId':cursor[4],'role':cursor[5]}
    
    data = json.dumps(datum)
    user = json.loads(data)
    
    username = user["username"]
    payload = {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60 * 60) # Token expires in 1 hour
        }
    token = jwt.encode(payload,app.config['SECRET_KEY'],algorithm = 'HS256')
    return jsonify({'token':token})
    
        
if __name__ == '__main__':
    app.run(debug=True) 