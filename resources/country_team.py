from flask_restful import Resource,reqparse
from db import query,uuid_hex
from flask_jwt_extended import jwt_required,get_jwt_claims


class CountryTeam(Resource):
    @jwt_required
    def post(self):
        user_type=get_jwt_claims()["user_type"]
        parser=reqparse.RequestParser()
        parser.add_argument('player_name',type=str,required=True,help="Enter player Name")
        parser.add_argument('category',type=str,required=True,help="Enter player category")
        parser.add_argument('country',type=str,required=True,help="Enter country name")
        parser.add_argument('points',type=int,required=True,help='Enter player points')
        data=parser.parse_args()
        player_id=uuid_hex()
        try:
            if user_type=='admin':
                query(f"""INSERT INTO country_team VALUES('{player_id}','{data['player_name']}','{data['category']}','{data['points']}','{data['country']}')""")
            else:
                return {'message':"Only admin can add players"}

        except:
            return {'message':'Sorry values are not inserted to db'},500
        return {'message':'Values inserted successfully'},201
