"""
Temp Script to create database with initialized data
"""
from server import db
from server import User
from server import Chore
import os
import cPickle as pickle
from chore_state import Chore_Status_Stack
from firebase import firebase


# Remove database file if it already exists
try:
	if os.stat("server.db"):
	   os.remove("server.db")
except:
	"Print server.db not found"	

# Remove chore_state if it already exists
try:
	if os.stat("chore_state.p"):
	   os.remove("chore_state.p")
except:
	"Print server.db not found"	

status_stack = Chore_Status_Stack()

with open("chore_state.p", "wb") as pickle_file:
	pickle.dump(status_stack, pickle_file)

# Create new database and add users
db.create_all()

mow_lawn = Chore(title="Mow Lawn", description="Mow the lawn and dump the clippings into a Yard Waste Bag.", salary=20.00, image_path="mow_lawn", status="not-completed")

empty_dishwasher = Chore(title="Empty Dishwasher", description="Empty AND Refill the dishwasher.  Remember to prewash!", salary=5.00, image_path="empty_dishwasher", status="not-completed")

vacuum_family_room = Chore(title="Vacuum Family Room", description="Do not forget the corners!  Also move the couch when you go to vacuum!", salary=5.00, image_path="vacuum_family_room", status="not-completed")

clean_bathrooms = Chore(title="Clean Bathrooms", description="Not just the toilet bowl, but around the toilet too.  This includes the bathroom mirror.", salary=10.00, image_path="clean_bathrooms", status="not-completed")

take_dog_for_walk = Chore(title="Take Dog for Walk", description="Get some exercise and give Fluffy some exercise while you are at it.", salary=2.00, image_path="take_dog_for_walk", status="not-completed")

get_an_A = Chore(title="Get an A", description="$2 per A at the end of the year.", salary=2.00, image_path="get_an_a", status="not-completed")

sweep_garage = Chore(title="Sweep Garage", description="Do not just sweep the leaves out of the garage, pick them up!", salary=5.00, image_path="sweep_garage", status="not-completed")

roll_over = Chore(title="Roll Over", description="Do a barrel roll!", salary=100.00, image_path="roll_over", status="not-completed")


# Create child objects
maggie = User(username="maggie", password="maggie", is_child=1, user_stage=2, full_name="Maggie Simpson", children=[], chores=[mow_lawn, empty_dishwasher, roll_over, vacuum_family_room, clean_bathrooms, take_dog_for_walk, get_an_A, sweep_garage])
lisa = User(username="lisa", password="lisa", is_child=1, user_stage=2, full_name="Lisa Simpson", children=[], chores=[mow_lawn, empty_dishwasher, roll_over, vacuum_family_room, clean_bathrooms, take_dog_for_walk, get_an_A, sweep_garage])
bart = User(username="bart", password="bart", is_child=1, user_stage=3, full_name="Bart Simpson", children=[], chores=[mow_lawn, empty_dishwasher, roll_over, vacuum_family_room, clean_bathrooms, take_dog_for_walk, get_an_A, sweep_garage])
evan = User(username="evan", password="child", is_child=1, user_stage=1, full_name="Evan Schaal", children=[], chores=[mow_lawn, empty_dishwasher, roll_over, vacuum_family_room, clean_bathrooms, take_dog_for_walk, get_an_A, sweep_garage])
future1 = User(username="future1", password="future1", is_child=1, user_stage=2, full_name="Future Grandgenett", children=[], chores=[mow_lawn, empty_dishwasher, roll_over, vacuum_family_room, clean_bathrooms, take_dog_for_walk, get_an_A, sweep_garage])
future2 = User(username="future2", password="future2", is_child=1, user_stage=3, full_name="Future South", children=[], chores=[mow_lawn, empty_dishwasher, roll_over, vacuum_family_room, clean_bathrooms, take_dog_for_walk, get_an_A, sweep_garage])

# Create parent objects
ryan = User(username="ryan", password="ryan", is_child=0, user_stage=0, full_name="Ryan Grandgenett", children=[future1], chores=[])
adam = User(username="adam", password="adam", is_child=0, user_stage=0, full_name="Adam Schaal", children=[evan, bart, lisa], chores=[])
josiah = User(username="josiah", password="test123", is_child=0, user_stage=0, full_name="Josiah South", children=[future2], chores=[])
homer = User(username="homer", password="homer", is_child=0, user_stage=0, full_name="Homer Simpson", children=[bart, maggie, lisa], chores=[])
marge = User(username="marge", password="marge", is_child=0, user_stage=0, full_name="Marge Simpson", children=[bart, maggie, lisa], chores=[])

# Add the objects to the database
db.session.add(mow_lawn)
db.session.add(roll_over)
db.session.add(empty_dishwasher)
db.session.add(vacuum_family_room)
db.session.add(clean_bathrooms)
db.session.add(take_dog_for_walk)
db.session.add(get_an_A)
db.session.add(sweep_garage)
db.session.add(maggie)
db.session.add(lisa)
db.session.add(bart)
db.session.add(evan)
db.session.add(adam)
db.session.add(future1)
db.session.add(future2)
db.session.add(ryan)
db.session.add(josiah)
db.session.add(homer)
db.session.add(marge)

db.session.commit()

parents = User.query.filter_by(is_child=0)
children = User.query.filter_by(is_child=1)
chores = Chores.query.all()

for child in children:
	for chore in chores:
		account = "/chores/{0}".format(username)
        chore_fb = {chore.title: chore.status}
        fb_connect = firebase.FirebaseApplication('https://popping-fire-3662.firebaseio.com', None)
        result = fb_connect.patch(account, chore_fb, {'print': 'pretty'}, {'X_FANCY_HEADER': 'VERY FANCY'})
        print result


