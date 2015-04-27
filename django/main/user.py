from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.conf import settings
import json
from hashlib import md5

import logging
logger = logging.getLogger(__name__)


class User(object):
  def __init__(self, id, competencies):
    #logger.info('User' + str(id))
    self.id = id
    self.name = ""
    testEmail = "stephane.collot@gmail.com"
    self.hash = md5(testEmail.strip().lower()).hexdigest() #use for profile picture
    self.competencies = {}
    for comp in competencies:
      self.competencies[comp] = 0
    
  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)