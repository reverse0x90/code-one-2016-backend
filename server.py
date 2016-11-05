from flask import Flask, request
from flask_restful import Resource, Api
from flask_cors import CORS, cross_origin
from sql.sql import SQL
import json

app = Flask(__name__)
CORS(app)
api = Api(app)
db = SQL()

# Check login credentials
class Login(Resource):
    def post(self):
      # Receive the login data
      login_data = request.get_json()
      input_username =(login_data["username"]).lower()
      input_password = login_data["password"]
      if db.valid_user(input_username):
        user = db.get_user(input_username)
        if user.password == input_password:
          if user.is_child:
            return {"username": user.username, "isChild": user.is_child, "userStage": user.user_stage, "fullName": user.full_name} 
          else:
             return {"username": user.username, "isChild": user.is_child, "fullName": user.full_name} 
      return {"status":"Login Failed :'("}


api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
