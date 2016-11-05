#!/usr/bin/python -tt
import os
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

# Get path of script
path = os.path.dirname(os.path.abspath(__file__)) 
engine = create_engine('sqlite:///{0}/server.db'.format(path))
Base = declarative_base()
 
class User(Base):
  """
  Reprsents a User Object
  """
  __tablename__ = "users"

  id = Column(Integer, primary_key=True)
  username = Column(String, unique=True)
  password = Column(String)
  is_child = Column(Integer)
  user_stage = Column(Integer, default=0)
  full_name = Column(String)

  def __init__(self, username, password, is_child, user_stage, full_name):
    """
    """
    self.username = username
    self.password = password
    self.is_child = is_child
    self.user_stage = user_stage
    self.full_name = full_name  
 
# create table
Base.metadata.create_all(engine)

