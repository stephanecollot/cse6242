from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.conf import settings
import json

import logging
logger = logging.getLogger(__name__)


class Competency(object):
  def __init__(self, text, score):
    #logger.info('User' + str(id))
    self.text = text
    self.score = score
    
  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class User(object):
  def __init__(self, id):
    #logger.info('User' + str(id))
    self.id = id
    self.competencies = []
    
  def toJSON(self):
    return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)