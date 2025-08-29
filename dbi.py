#!/usr/bin/python3

import mysql.connector
import yaml

dbi_config = yaml.safe_load(open('/home/asc/dev/asc-system/.config/dbi_config.yml'))
dbi_config['ssl_disabled']=True

def query_db(query, params=None):
  cnx = mysql.connector.connect(**dbi_config)
  cursor = cnx.cursor()
  cursor.execute(query, params)

  result = []
  for row in cursor:
    result.append(row)

  cursor.close()
  cnx.close()

  return result






