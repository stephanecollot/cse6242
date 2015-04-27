from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.conf import settings
import json
from user import User
from postgresql import connection
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
  
  if len(request.session['competencies']) > 0:
  
    db = sqlite3.connect("main/Sover.db")
    where = ""
    j = len(request.session['competencies'])
    for comp in request.session['competencies']:
      if j==0:
        break
      elif j ==1:
        where = where+ 'tag like "'+comp+'"'
      else:
        where = where+ 'tag like "'+comp+'" or '
      j = j-1
    limit = len(request.session['competencies']) * 10
    query = "SELECT * FROM tagscore WHERE "+where+" GROUP BY userid, tag ORDER BY score DESC LIMIT "+str(limit)
    print query
    rows = db.execute(query)
    
    users = {}
    for row in rows:
      id = row[0]
      comp = row[1]
      score = row[2]
      if id in users:
        users[id].competencies[comp] = score
      else:
        user = User(id, request.session['competencies'])
        user.competencies[comp] = score
        user.getInfo()
        users[id] = user
    
    result = {}
    result['users'] = users.values()
    result['competencies'] = request.session['competencies']
    
  else:
    result = {}
    result['users'] = []
    result['competencies'] = []
  
  result_json = json.dumps(result, default=lambda o: o.__dict__)
  response = HttpResponse(result_json, content_type='application/json')
  response.__setitem__("Access-Control-Allow-Origin", "*") #enables CORS (required to use json)
  return response

def userprofile(request, uid):
  print "Received UserProfile request: " + uid

  db = sqlite3.connect("main/Sover.db")
  print db.iterdump()
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
 
  result = g
  result_json = json.dumps(result, default=lambda o: o.__dict__)
  response = HttpResponse(result_json, content_type='application/json')
  response.__setitem__("Access-Control-Allow-Origin", "*") #enables CORS (required to use json)
  return response

