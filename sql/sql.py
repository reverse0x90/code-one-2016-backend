#!/usr/bin/python -tt
import os
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from table_def import User

# Get path of script
path = os.path.dirname(os.path.abspath(__file__))


class SQL(object):
  """
  Represents a SQL object. The object is used to insert new contacts into the rolodex.
  """

  def __init__(self):
    """Returns a SQL object"""
    self.engine = create_engine('sqlite:///{0}/server.db'.format(path))
    self.Session = sessionmaker(bind=self.engine)
    self.session = self.Session()
    
  #
  # User account sql functions
  #
  def add_user(self, username, password, is_child, user_stage, full_name):
    """Adds user to the database"""
    try:
      new_user = User(username, password, is_child, user_stage, full_name)
      self.session.add(new_user)
      self.session.commit()
    except exc.IntegrityError:
       self.session.rollback()
       print "[-] Error adding new user account %s" % (username)

  def get_user(self, username):
    """Returns user information from the database"""
    try:
      user = self.session.query(User).filter(User.username==username).first()
      return user
    except:
      print "[-] User %s not found!" % (username)
      return False

  def set_user(self, user_object):
    """Modifies user in the database"""
    try:
      user = self.session.query(User).filter(User.username==user_object.username).first()
      user.password = user_object.password
      user.is_child = user_object.is_child
      user.full_name = user_object.full_name
      self.session.commit()
    except exc.IntegrityError:
       self.session.rollback()
       print "[-] Error modifying user account %s" % (user_object.username)
    
  def delete_user(self, user_object):
    """Deletes user in the database"""
    try:
      #user = self.session.query(User).filter(User.username==user_object.username).first()
      self.session.delete(user_object)
      self.session.commit()
    except:
       self.session.rollback()
       print "[-] Error removing user account %s" % (user_object.username)

  def valid_user(self, username):
    """Returns if user information is the database"""
    try:
      user = self.session.query(User).filter(User.username==username).first()
      if user.username:
        return True
      else:
        return False
    except:
      print "[-] User %s not found!" % (username)
      return False


