"""
Temp Script to create database with initialized data
"""
from server import db
from server import User
import os

# Remove database file is already exists
try:
	if os.stat("server.db"):
	   os.remove("server.db")
except:
	"Print server.db not found"	

# Create new database and add users
db.create_all()

# Create child objects
maggie = User(username="maggie", password="maggie", is_child=1, user_stage=2, full_name="Maggie Simpson", children=[])
lisa = User(username="lisa", password="lisa", is_child=1, user_stage=2, full_name="Lisa Simpson", children=[])
bart = User(username="bart", password="bart", is_child=1, user_stage=3, full_name="Bart Simpson", children=[])
evan = User(username="child1", password="child", is_child=1, user_stage=1, full_name="Evan Schaal", children=[])
future1 = User(username="future1", password="future1", is_child=1, user_stage=2, full_name="Future Grandgenett", children=[])
future2 = User(username="future2", password="future2", is_child=1, user_stage=3, full_name="Future South", children=[])

# Create parent objects
ryan = User(username="ryan", password="ryan", is_child=0, user_stage=0, full_name="Ryan Grandgenett", children=[future1])
adam = User(username="adam", password="adam", is_child=0, user_stage=0, full_name="Adam Schaal", children=[evan])
josiah = User(username="josiah", password="test123", is_child=0, user_stage=0, full_name="Josiah South", children=[future2])
homer = User(username="homer", password="homer", is_child=0, user_stage=0, full_name="Homer Simpson", children=[bart, maggie, lisa])
marge = User(username="marge", password="marge", is_child=0, user_stage=0, full_name="Marge Simpson", children=[bart, maggie, lisa])

# Add the objects to the database
db.session.add(maggie)
db.session.add(lisa)
db.session.add(bart)
db.session.add(evan)
db.session.add(adam)
db.session.add(future1)
db.session.add(future2)
db.session.add(ryan)
db.session.add(adam)
db.session.add(josiah)
db.session.add(homer)
db.session.add(marge)
db.session.commit()

parents = User.query.filter_by(is_child=0)
children = User.query.filter_by(is_child=1)

print "\n\n===Parents of children in the database===\n"
for parent in parents:
	print "{0}:".format(parent.full_name)
	for child in parent.children:
		print "\t{0}".format(child.full_name)
	print "\n"

print "\n\n===Children of parents in the database===\n"
for child in children:
	print "{0}:".format(child.full_name)
	for parent in child.parents:
		print "\t{0}".format(parent.full_name)
	print "\n"

 parents = User.query.filter_by(parents=homer).distinct()