from flask import Flask, request
from flask_restful import Resource, Api
from sql.sql import SQL
import json

app = Flask(__name__)
api = Api(app)
db = SQL()

class Login(Resource):
    def post(self):
      login_data = request.get_json()
      if db.valid_user(login_data["username"]):
        user = db.get_user(login_data["username"])
        if user.password == login_data["password"]:
          if user.is_child:
            return {"username": user.username, "isChild": user.is_child, "userStage": user.user_stage, "fullName": user.full_name} 
          else:
             return {"username": user.username, "isChild": user.is_child, "fullName": user.full_name} 
      return {"Login":"Failed"}


api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
