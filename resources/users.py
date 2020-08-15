from flask_restful import Resource ,reqparse
from werkzeug.security import safe_str_cmp
from db import query,uuid_hex
from flask_jwt_extended import create_access_token

class User():
    def __init__(self,user_id,user_password,user_type):
        self.user_id=user_id
        self.user_password=user_password
        self.user_type=user_type

    @classmethod
    def getUserByName(cls,user_name):
        result=query(f"""SELECT user_id,user_password,user_type FROM user_details WHERE user_name='{user_name}' """,return_json=False)
        if len(result)>0:
            return User(result[0]['user_id'],result[0]['user_password'],result[0]['user_type'])
        return None




class UserRegister(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument("user_password",type=str,required=True,help="Enter a valid password rey")
        parser.add_argument("user_name",type=str,required=True,help="User name pampi raaa")
        parser.add_argument("user_type",type=str,required=True,help="User type pampi raaa")
        data=parser.parse_args()
        try:
            id=uuid_hex()
            if len(query(f"""SELECT * FROM user_details WHERE user_name='{data['user_name']}'""",return_json=False))>0 :
                return {'message':'Name already exists. Please use an other one'},400
            query(f"""INSERT INTO user_details VALUES('{id}','{data['user_password']}','{data['user_name']}','{data['user_type']}')""")
        except:
            return {'message':'There is an error dumbass'},500
        return {'message':'values have been inserted'},201

class UserLogin(Resource):
    def post(self):
        parser=reqparse.RequestParser()
        parser.add_argument('user_name',type=str,required=True,help="Check your user name")
        parser.add_argument("user_password",type=str,required=True,help="Enter valid password")
        parser.add_argument("user_type",type=str,required=True,help="check user/admin login")
        data=parser.parse_args()
        userobj=User.getUserByName(data['user_name'])
        if userobj and safe_str_cmp(userobj.user_password,data['user_password']) and data['user_type']==userobj.user_type:
            token=create_access_token(identity=userobj.user_id,expires_delta=False)
            return {'access_token':token},200
        return {'message':'Invalid Credentials'}
