from django.conf import settings
import json
from user import User
import psycopg2
#from db import * #db.py file for ID

import logging
logger = logging.getLogger(__name__)


def connection():
  logger.info('PostgreSQL')

  try:
    conn = psycopg2.connect(database=db_name, user=db_user, password=db_password, host=db_host, port=db_port)
  except:
    print "I am unable to connect to the database"
  
  cur = conn.cursor()
  cur.execute("""SELECT * FROM Users LIMIT 2""")
  rows = cur.fetchall()
  
  print "\nShow me the databases:\n"
  for row in rows:
    print "   ", row[3]
  
  
 