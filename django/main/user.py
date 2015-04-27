from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.conf import settings
import json
from hashlib import md5
import sqlite3

import logging
logger = logging.getLogger(__name__)


class User(object):
  def __init__(self, id, competencies):
    #logger.info('User' + str(id))
    self.id = id
    self.name = ""
    self.email = "stephane.collot@gmail.com"
    self.hash = md5(self.email.strip().lower()).hexdigest() #use for profile picture
    self.competencies = {}
    for comp in competencies:
      self.competencies[comp] = 0
      
  def getInfo(self):
    db = sqlite3.connect("main/Sover.db")
    rows = db.execute("SELECT name FROM user WHERE uid="+str(self.id))
    
    for row in rows:
      self.name = row[0]
      self.email = self.name+"@gmail.com" # Try to fake an email
      self.hash = md5(self.email.strip().lower()).hexdigest()
    
  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)