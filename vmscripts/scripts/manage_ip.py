from pgsql_conn import *
import datetime
import pytz

dbConn = create_connection('postgres', '127.0.0.1', 'postgres', 'postgres')

def get_free_ip():
  freeIPRow = select(dbConn, 'ip_lists', 'ip_addr', "WHERE free is true ORDER BY ID LIMIT 1")
  freeIP = ""
  if len(freeIPRow) != 0:
    freeIP = freeIPRow[0]['ip_addr']
  return freeIP

def allotIP(ip_addr, mac_lists_id):
  update (dbConn, 'ip_lists', {'mac_lists_id' : mac_lists_id, 'free' : 'f'},
    "ip_addr='{}'".format(ip_addr))

def releaseIP(ip_addr):
  update (dbConn, 'ip_lists', {'mac_lists_id' : None, 'free' : 't' }, "ip_addr='{}'".format(ip_addr))
