from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required,get_jwt_claims
from db import query

class UserMatch(Resource):
    @jwt_required
    def get(self):
        user_type=get_jwt_claims()['user_type']
        if user_type=='admin':
            return {'message':'login as user :p'}
        parser=reqparse.RequestParser()
        parser.add_argument('user_name',type=str,required=True,help="Error in getting user id")
        data=parser.parse_args()
        try:
            played=query(f"""SELECT match_id FROM user_team WHERE user_id='{data['user_name']}'""",return_json=False)
        except:
            return {'message':'Error while collecting the matches played by user '}

        print(played)
        # try:
        #     query(f"""SELECT match_id FROM match_user WHERE match_id not in('{played[0]}')""")
