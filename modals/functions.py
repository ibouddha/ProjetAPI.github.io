import modals.connect as connect
from flask import json,request,jsonify,session
import modals.functions as func


def login(username,password):
    """This function checks if the username and password are correct.
    If they are, it returns True. If not, it returns False.
    """
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users where username=%s and password=%s',(username,password))
    result = cursor.fetchone()
    if result:
        return result
    else:
        return False

def auth():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    # if not username or not password:
    #         return jsonify({'error': 'Missing username or password'}), 400

    cursor = func.login(username,password)
    if not cursor:
        return jsonify({'error': 'Invalid username or password'}), 400

    datum = {'id':cursor[0],'username':cursor[1],'password' : cursor[2],'email':cursor[3],'groupeId':cursor[4],'role':cursor[5]}

    data = json.dumps(datum)
    user = json.loads(data)
    if user['role']=='admin':
        session['username'] = user['username']
        return user['username']
    
def add_user(user_id,username,password,email,groupeId,role):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users values (%s,%s,%s,%s,%s,%s)")
    conn.commit()
    cursor.close()
    
def count():
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM users")
    result = cursor.fetchone()
    if result:
        return result
    else:
        return 0
    
def getUser(username):
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute('SELECT * from users where username = %s',(username,))
    user = cursor.fetchone()
    if user:
        return {'user':{'id':user[0],'username':user[1],'password':user[2],'email':user[3],'groupe_id':user[4],'role':user[5]}}
    else:
        return {"user": "404 no User with this name"}
    
def updateuser(user):
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET email = %s, id_groupe = %s,role = %s",(user["email"],user["groupe_id"],user["role"]))
    conn.commit()
    cursor.close()
    
def deleteuser(user):
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s",(user["id"],))
    conn.commit()
    cursor.close()

def deleteprompt(id_prompt):
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prompt WHERE id = %s",(id_prompt,))
    conn.commit()
    cursor.close()

def add_prompt(prompt):
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO prompt values (%s,%s,%s,%s,%s,%s)",(prompt['id'],prompt['content'],prompt['prix'],prompt['status'],session['user_id']))
    conn.commit()
    cursor.close()

def updatePrompt(prompt):
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE prompt SET content = %s, prix = %s, status = %s",(prompt['content'],prompt['prix'], prompt['status']))
    conn.commit()
    cursor.close()

#delete prompt
def deletePrompt(id_prompt):
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM prompt WHERE id = %s",(id_prompt,))
    conn.commit()
    cursor.close()

#get all prompts
def getAllPrompts():
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prompt")
    prompts = cursor.fetchall()
    cursor.close()
    return prompts

#admin ask for update
def getPrompt(id_prompt):
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prompt WHERE id = %s",(id_prompt,))
    prompt = cursor.fetchone()
    cursor.close()
    return prompt

#update status of prompt
def updateStatus(id_prompt,status):
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE prompt SET status = %s WHERE id = %s",(status,id_prompt,))
    conn.commit()
    cursor.close()

#Validate prompt
def validatePrompt(id_prompt):
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE prompt SET status = 'validé' WHERE id = %s",(id_prompt))
    conn.commit()
    cursor.close()

#Proposer des prompts à vendre
def proposePrompt(id_prompt):
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE prompt SET status = 'proposé' WHERE id = %s",(id_prompt))
    conn.commit()
    cursor.close()
    
#afficher les prompts proposés à vendre
def getProposedPrompts():
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM prompt WHERE status = 'proposé'")
    prompts = cursor.fetchall()
    cursor.close()
    return prompts

#Voter pour l'activation des prompts en attente.
def votePrompt(id_prompt):
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE prompt SET status = 'voté' WHERE id = %s",(id_prompt))
    conn.commit()
    cursor.close()
    
#Noter les prompts activés (sauf les leurs)
def notePrompt(id_prompt,user_id,note):
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE prompt SET note = %s WHERE id = %s and user_id != %s",(note,id_prompt,user_id))
    conn.commit()
    cursor.close()
    
#Les membres d'un même groupe ont un impact plus fort sur les notes et les votes
def notePromptGroup(id_prompt,user_id,note):
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE prompt SET note = %s WHERE id = %s and user_id =%s ",(note,prompt_id,user_id))
    conn.commit()
    cursor.close()
    
def votePromptGroup(id_prompt,user_id,vote):
    conn = connect.connect()
    cursor = conn.cursor()
    cursor.execute("UPDATE prompt SET vote = %s WHERE id = %s and user_id =%s",(vote,id_prompt,user_id))
    conn.commit()
    