import modals.connect as connect

def login(username,password):
    cursor = connect.connect()
    cursor.execute('SELECT * from users where username=%s and password=%s',(username,password,))
    user= cursor.fetchone()
    return user