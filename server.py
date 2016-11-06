from flask import Flask, request
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from firebase import firebase


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


user_to_chores = db.Table('user_to_chores', db.Model.metadata,
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
    db.Column("chore_id", db.Integer, db.ForeignKey("chore.id"))
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
  chores = db.relationship("Chore", secondary=user_to_chores)
  

  def __init__(self, username, password, is_child, user_stage, full_name, children, chores):
    self.username = username
    self.password = password
    self.is_child = is_child
    self.user_stage = user_stage
    self.full_name = full_name
    self.children = children
    self.chores = chores

class Chore(db.Model):
  __tablename__ = 'chore'
  id = db.Column(db.Integer, primary_key=True)
  #parent_id = db.Column(db.Integer,db.ForeignKey('user.id'))
  title = db.Column(db.String(250), unique=True)
  description = db.Column(db.Text)
  salary = db.Column(db.Float)
  image_path = db.Column(db.Text)
  status = db.Column(db.String(250))

  def __init__(self, title, description, salary, image_path, status):
    self.title = title
    self.description = description
    self.salary = salary
    self.image_path = image_path
    self.status = status

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
        active_user = {"username": user.username, "isChild": user.is_child, "fullName": user.full_name}
        for parent in user.parents:
          for child in parent.children:
            if child not in children:
              children.append(child)
          if parent not in parents:
            parents.append(parent)
      else:
        active_user = {"username": user.username, "isChild": user.is_child, "userStage": user.user_stage, "fullName": user.full_name}
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
      return {"active_user": active_user, "parents": out_parents, "children": out_children}

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

# Check login credentials
class Get_All_Chores(Resource):
  def get(self):
    chores = Chore.query.all()
    chores_array = []
    for chore in chores:
      chores_array.append({"title":chore.title, "description": chore.description, "salary": chore.salary, "image_path": chore.image_path, "status": chore.status}) 
    return {"chores": chores_array}

# Get all possible user chores
class Get_User_Chores(Resource):
  def get(self, username):
     # Look for user in the database
      user = User.query.filter_by(username=username).first()
      chores_array = []
      if user:
         for chore in user.chores:
          chores_array.append({"title":chore.title, "description": chore.description, "salary": chore.salary, "image_path": chore.image_path, "status": chore.status}) 
      return {"chores": chores_array}

# Update Account 
class Update_Acount(Resource):
  def post(self, username, value):
    try:
      account = "/account/{0}".format(username)
      funds = {"balance": float(value)}
      # Look for user in the database
      fb_connect = firebase.FirebaseApplication('https://popping-fire-3662.firebaseio.com', None)
      result = fb_connect.patch(account, funds, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
      return {"status": "Success", "Message": "Firebase updated success"}
    except:
     return {"status": "Error", "Message": "Firebase updated failure"}

# Update Account 
class Update_Stage(Resource):
  def get(self, username, stage):
    user = User.query.filter_by(username=username).first()
    if user:
      pass
     return {"status": "Error", "Message": "Firebase updated failure"}
    
    

api.add_resource(Login, '/login')
api.add_resource(Login, '/login')
api.add_resource(Login, '/login')
api.add_resource(Get_All_Chores, '/chores')
api.add_resource(Get_User_Chores, '/chores/<string:username>')
api.add_resource(Update_Acount, '/update/account/<string:username>/<string:value>')
api.add_resource(Update_Stage, '/update/<string:username>/<string:stage>')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
