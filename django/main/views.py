from django.shortcuts import render
from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.conf import settings
import json
from user import User, Competency
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
  print request
  db = sqlite3.connect("Sover.db")
  x = ""
  j = len(request)
  for i in request:
    if j==0:
      break
    elif j ==1:
      x = x+ 'tag like "'+i+'"'
    else:
      x = x+ 'tag like "'+i+'" or '
    j = j-1
  num = len(request) * 20
  y = db.execute("select * from tagscore where "+x+" group by userid, tag limit "+str(num))
  users = {}
  foo = []
  for i in y:
    foo.append(i)

  for i in range foo:
    #this is the list which has tuples in the form of (userid,tag,score)


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

