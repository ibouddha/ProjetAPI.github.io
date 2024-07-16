import modals.connect as connect
import modals.functions as func
from flask import Blueprint,request,json,session,jsonify

user_bp = Blueprint("users",__name__)

@user_bp.route('/addPrompt',methods=["GET","POST"])
def addPrompt():
    if request.method == 'POST':
        data = request.get_json()
        print(data)
        try:
            func.add_prompt(data)
            return jsonify({'added successfully'})
        except:
            return jsonify({'error': 'error in adding prompt'})
    
@user_bp.route('/findAllPrompt',methods=["POST","GET"])
def getAllPrompts():
    prompts = func.getAllPrompts()
    if(len(prompts)>=1):
        return prompts
    else:
        print("there is no prompt")
        return False
    