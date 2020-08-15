from flask import Flask,jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager
from db import query
from resources.users import UserRegister,UserLogin
from resources.country_team import CountryTeam
from resources.match_user import GetCountries,CreateMatch
from resources.match_perfomance import MatchPerfomance
from resources.admin_team import CountryPlayers
from resources.match_selection import UserMatch
# from resources.player_selection import PointsValidation,UserTeam


app=Flask(__name__)
app.config["JWT_SECRET_KEY"]="$#@!"
app.config['PROPAGATE_EXCEPTIONS']=True

api=Api(app)
jwt=JWTManager(app)


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        'error': 'authorization_required',
        "description": "Request does not contain an access token."
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    return jsonify({
        'error': 'invalid_token',
        'description': 'Signature verification failed.'
    }), 400



@jwt.user_claims_loader
def add_claims_to_access_token(identity):
    return {'user_type':query(f"""SELECT user_type FROM user_details WHERE user_id='{identity}'""",return_json=False)[0]['user_type']}




api.add_resource(CountryTeam,"/add_player")
api.add_resource(UserRegister,"/register")
api.add_resource(UserLogin,"/login")
api.add_resource(GetCountries,'/get_countries')
api.add_resource(CreateMatch,"/create_match")
api.add_resource(MatchPerfomance,"/match_performance")
api.add_resource(CountryPlayers,"/admin_team")
api.add_resource(UserMatch,'/user_match_selection')
# api.add_resource(UserTeam,"/user_team")
# api.add_resource(PointsValidation,"/points_validation")



if __name__=="__main__":
    app.run()
