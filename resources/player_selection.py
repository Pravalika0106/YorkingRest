from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required,get_jwt_claims
from db import query


class UserTeam(Resource):
    @jwt_required
    def get(self):
        user_type=get_jwt_claims()['user_type']
        if user_type=='admin':
            return {'message':'login as user :p'}
        parser=reqparse.RequestParser()
        parser.add_argument('match_id',type=str,required=True,help="Error while getting match id")
        data=parser.parse_args()
        try:
            countries=query(f"""SELECT country1,country2 FROM  match_user WHERE match_id='{data['match_id']}'""",return_json=False)
        except:
            return {'message':'Error while getting the countries of the match'}
        try:
            players= query(f"""SELECT player_id FROM country_team WHERE country in('{countries[0]['country1']}',
            '{countries[0]['country2']}')""")
            return players
        except:
            return {'message':'Error while getting the players of the countries'}

class PointsValidation(Resource):
    selection=False
    @jwt_required
    def post(self):
        selection=False
        parser=reqparse.RequestParser()
        # Handle no of players = 11 In the front end
        parser.add_argument('player1',type=str,required=True,help="Error while getting player1 id")
        parser.add_argument('player2',type=str)
        parser.add_argument('player3',type=str)
        parser.add_argument('player4',type=str)
        parser.add_argument('player5',type=str)
        parser.add_argument('player6',type=str)
        parser.add_argument('player7',type=str)
        parser.add_argument('player8',type=str)
        parser.add_argument('player9',type=str)
        parser.add_argument('player10',type=str)
        parser.add_argument('player11',type=str)
        parser.add_argument('match_id',type=str,required=True,help="Error while getting match id")
        parser.add_argument('user_id',type=str,required=True,help="Error while getting user id")
        #CAPTAIN SELECTION REQUIRED........
        parser.add_argument('captain',type=str,required=True,help="Error while getting the captain")
        #STAR CALCULATION REQUIRED.............
        parser.add_argument('star',type=str,required=True,help="Error while getting the stars of the team selected")
        data=parser.parse_args()
        points=100
        for i in range(1,12):
            key=f"""player{i}"""
            if data[key]==None:
                break;
            if points<0:
                break;
            val=query(f"""SELECT points FROM country_team WHERE player_id='{data[key]}'""",return_json=False)[0]
            points-=val['points']
        if points<0:
            return {'message':"Points exceeded limit of 100. Please choose below 100 only"}

        #UPDATING USER TEAM TABLE
        try:
            query(f"""INSERT INTO user_team VALUES('{data['captain']}','{data['stars']}','{data['user_id']}','{data['match_id']}')""")
        except:
            return {'message':"Error in updating the user team table"}

        points=100
        for i in range(1,12):
            key=f"""player{i}"""
            if data[key]==None:
                break;
            # try:
            query(f"""INSERT INTO choosen_players VALUES('{data['user_id']}','{data['match_id']}','{data[key]}')""")
            # except:
            #     return {'message':'Error in inserting choosen players to db'}
            # return {'message':'Choosen Players Inserted'}
