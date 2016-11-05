from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///server.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)
api = Api(app)


#Table to handle the self-referencing many-to-many relationship for the User class:
#First column holds the user who is a parent, the second the user is the child.
user_to_user = db.Table('user_to_user',
    db.Column("parent_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("child_id", db.Integer, db.ForeignKey("user.id"), primary_key=True)
)


class User(db.Model):
  __tablename__ = 'user'
  id = db.Column(db.Integer, primary_key=True)
  #parent_id = db.Column(db.Integer,db.ForeignKey('user.id'))
  username = db.Column(db.String(250), unique=True)
  password = db.Column(db.String(250))
  is_child = db.Column(db.Integer)
  user_stage =  db.Column(db.Integer)
  full_name = db.Column(db.String(250))
  children = db.relationship("User",
                    secondary=user_to_user,
                    primaryjoin=id==user_to_user.c.parent_id,
                    secondaryjoin=id==user_to_user.c.child_id,
                    backref="parents"
    )

  def __init__(self, username, password, is_child, user_stage, full_name, children):
    self.username = username
    self.password = password
    self.is_child = is_child
    self.user_stage = user_stage
    self.full_name = full_name
    self.children = children


# Check login credentials
class Login(Resource):
    def _seralize_user(self, user):
      parents = []
      children = []
      out_parents = []
      out_children = []

      # If the user is a child get its parents. Else get the parents children
      # This will need to be improved inorder to scale
      if user.is_child:
        for parent in user.parents:
          for child in parent.children:
            if child not in children:
              children.append(child)
          if parent not in parents:
            parents.append(parent)
      else:
        for child in user.children:
          for parent in child.parents:
            if parent not in parents:
              parents.append(parent)
          if child not in children:
            children.append(child)

      # Now we have the list of children and parents
      for parent in parents:
        out_parents.append({"username": parent.username, "isChild": parent.is_child, "fullName": parent.full_name})

      for child in children:
        out_children.append({"username": child.username, "isChild": child.is_child, "userStage": child.user_stage, "fullName": child.full_name})

      # Return the array of parents and children
      return {"active_user": user.username, "parents": out_parents, "children": out_children}

    def post(self):
      # Receive the login data
      login_data = request.get_json()
      # Pull out json data
      json_username =(login_data["username"]).lower()
      json_password = login_data["password"]

      # Look for user in the database
      user = User.query.filter_by(username=json_username).first()
      if user:
        if user.password == json_password:
          return self._seralize_user(user)
      return {"status":"Login Failed :'("}


api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
