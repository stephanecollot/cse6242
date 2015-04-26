from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.conf import settings
import json
from user import User, Competency
import sqlite3

import logging
logger = logging.getLogger(__name__)

# Create your views here.

def index(request):
  logger.info('It works! global ready:')
  
  if not 'competencies' in request.session:
    request.session['competencies'] = []
  
  return render_to_response('index.html')
  #return HttpResponse("Hello, world. Here is the index.")
  
  
def add(request, text):
  print "Received add request: " + text
  
  if 'competencies' in request.session:
    if not text in request.session['competencies']:
      request.session['competencies'].append(text)
  else:
    request.session['competencies'] = []
  request.session.modified = True
    
  print request.session['competencies']

  result = []
  result_json = json.dumps(result, default=lambda o: o.__dict__)
  response = HttpResponse(result_json, content_type='application/json')
  response.__setitem__("Access-Control-Allow-Origin", "*") #enables CORS (required to use json)
  return response
  
  
def remove(request, text):
  print "Received remove request: " + text
  
  if 'competencies' in request.session:
    if text in request.session['competencies']:
      request.session['competencies'].remove(text)
  else:
    request.session['competencies'] = []
  request.session.modified = True
    
  print request.session['competencies']
  
  result = []
  result_json = json.dumps(result, default=lambda o: o.__dict__)
  response = HttpResponse(result_json, content_type='application/json')
  response.__setitem__("Access-Control-Allow-Origin", "*") #enables CORS (required to use json)
  return response
  
def chart(request):
  print "Received chart request "
  
  user1 = User(1)
  user1.competencies.append(Competency('c++',11))
  user1.competencies.append(Competency('java',12))
  user2 = User(2)
  user2.competencies.append(Competency('c++',21))
  user2.competencies.append(Competency('java',25))
  
  result = []
  result.append(user1)
  result.append(user2)
  
  result_json = json.dumps(result, default=lambda o: o.__dict__)
  response = HttpResponse(result_json, content_type='application/json')
  response.__setitem__("Access-Control-Allow-Origin", "*") #enables CORS (required to use json)
  return response

def userprofile(uid):
  db = sqlite3.connect("Sover.db")
  x = db.execute("select tag, score from tagscore where userid ="+uid+" limit 7")
  f = {}
  for i in x:
    tag, score = i
    f[tag] = score
  g = {}
  g['radar'] = f
  x = db.execute("select * from user where uid ="+ uid)
  h={}
  for i in x:
    uid, name, date, location, rep = i
  h['uid'] = uid
  h['name'] = name
  h['date'] = date
  h['location'] = location
  h['rep'] = rep
  g['profile'] = h
  print g
