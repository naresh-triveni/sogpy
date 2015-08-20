from pgsql_conn import *
import datetime
import pytz

dbConn = create_connection('postgres', '127.0.0.1', 'postgres', 'postgres')


data = select(dbConn, 'vms', '*')


for dom in data:
  print "VM NAME : ", dom['domain_name']
  print "VCPU : ", dom['vcpu']
  print "Memory Size (in KB)", dom['memory_size']
  print "Start Time : ", dom['start_time']
  print " "