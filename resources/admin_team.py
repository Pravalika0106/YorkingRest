from flask_restful import Resource,reqparse
from db import query
from flask_jwt_extended import jwt_required,get_jwt_claims


class CountryPlayers(Resource):
    @jwt_required
    def get(self):
        user_type=get_jwt_claims()['user_type']
        if user_type=='user':
            return {'message':'No access to user'}
        parser=reqparse.RequestParser()
        parser.add_argument('match_id',type=str,required=True,help='Error in getting match id')
        data=parser.parse_args()
        # try:
        countries=query(f"""SELECT country1,country2 FROM match_user WHERE match_id='{data['match_id']}'""",return_json=False)
        # except:
        #     return {'messsage':'error in getting countries'}
        # print(countries[0]['country1'])
        # try:
        #     return query(f"""SELECT player_id,country FROM country_team WHERE country in('{countries[0]['country1']}',
        #     '{countries[0]['country2']}')""")
        # except:
        #     return {'message':'error in getting players of country one and country two'}
