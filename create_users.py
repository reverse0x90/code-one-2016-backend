"""
Temp Script for creating users in the database
"""

from sql.sql import SQL

db = SQL()

db.add_user(username="josiah", password="test123", is_child=0, user_stage=0, full_name="Josiah South")
db.add_user(username="adam", password="adam", is_child=0, user_stage=0, full_name="Adam Schaal")
db.add_user(username="ryan", password="ryan", is_child=0, user_stage=0, full_name="Ryan Grandgenett")
db.add_user(username="child1", password="child", is_child=1, user_stage=1, full_name="Evan Schaal")
db.add_user(username="child2", password="child", is_child=1, user_stage=2, full_name="Evan Schaal")
db.add_user(username="child3", password="child", is_child=1, user_stage=3, full_name="Evan Schaal")
