from flask_restful import Resource,reqparse
from db import query,uuid_hex
from flask_jwt_extended import jwt_required,get_jwt_claims

class GetCountries(Resource):
    @jwt_required
    def get(self):
        try:
            return query("SELECT DISTINCT country FROM country_team")
        except:
            return {'message':'Error while getting countries'},500

class CreateMatch(Resource):
    @jwt_required
    def post(self):
        user_type=get_jwt_claims()['user_type']
        if user_type =='user':
            return {'message':'Admin pages cannot be accessed'}
        parser=reqparse.RequestParser()
        parser.add_argument('country1',type=str,required=True,help='Check the value of country1')
        parser.add_argument('country2',type=str,required=True,help='Check the value of country2')
        parser.add_argument('match_status',type=str)
        match_id=uuid_hex()
        data=parser.parse_args()
        if data['country1']==data['country2']:
            return {'message':'Country one and country two cannot be same'},400
        try:
            if data['match_status']==None:
                query(f"""INSERT INTO match_user(match_id,country1,country2) VALUES('{match_id}','{data['country1']}','{data['country2']}')""")
            else:
                query(f"""INSERT INTO match_user VALUES('{match_id}','{data['country1']}','{data['country2']}','{data['match_status']}')""")
        except:
            return {'message':'Insertion failed'},500
        return {'message':'Insertion successfull'},201
