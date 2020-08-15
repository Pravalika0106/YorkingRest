from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required,get_jwt_claims
from db import query


class MatchPerfomance(Resource):
    @jwt_required
    def post(self):
        user_type=get_jwt_claims()['user_type']
        if user_type=='user':
            return {'message':'No access to User'}
        parser=reqparse.RequestParser()

        parser.add_argument('match_id',type=str,required=True,help="Error in getting match id")
        parser.add_argument('player_id',type=str,required=True,help="Error in getting player id")
        parser.add_argument('runs',type=int,required=True,help="Error in getting no of runs")
        parser.add_argument('catches',type=int,required=True,help='Error in getting no of catches')
        parser.add_argument('wickets',type=int,required=True,help="Error in getting no of wickets")
        data=parser.parse_args()
        print(data['player_id'])
        try:
            l=query(f"""SELECT * FROM match_perfomance WHERE match_id='{data['match_id']}'AND player_id='{data['player_id']}'""",return_json=False)
            print(l)
            if len(l)>0:
                return {'message':'player performance is already entered and cannot be updated'},401
        except:
            return {'message':'Error in accessing the match id and player id'},400
        print('Yes')
        try:
            query(f"""INSERT INTO match_perfomance VALUES('{data['runs']}','{data['catches']}','{data['wickets']}',
                                                          '{data['player_id']}','{data['match_id']}')""")
        except:
            return {'message':'Error while inserting values into database'},400
        return {'message','Values Inserted successfully'},201
