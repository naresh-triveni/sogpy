# prerequisite installations
# install pip using easyinstall,
# install virtualenv using pip, command is: pip install virtualenv
# go to your working directory, create a virtual environment, command is: virtualenv env, which creates a directory naming env in the same directory, then
# activate this environment, command is: env/bin/activate, being in your working directory
# then install Psycopg2 using pip, command is: pip install Psycopg2


import psycopg2
import psycopg2.extras
import sys

def create_connection(dbname, host, username, password):
  conn_string = "host='{}' dbname='{}' user='{}' password='{}'".format(host, dbname, username, password)
  conn = psycopg2.connect(conn_string)
  return conn

def select(conn, table_name, column_names, clause=None):
  work_mem = 2048
  cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
  cursor.execute('SET work_mem TO %s', (work_mem,))
  if clause:
    query = 'SELECT {} FROM {} {}'.format(column_names, table_name, clause)
  else:
    query = 'SELECT {} FROM {}'.format(column_names, table_name)

  cursor.execute(query)
  columns_query = """SELECT attname
  FROM   pg_attribute
    WHERE  attrelid = 'public.{}'::regclass
    AND    attnum > 0
    AND    NOT attisdropped
    ORDER  BY attnum;""".format(table_name)
  cursor.execute(columns_query)
  cnames = []
  cnames_to_fetch = column_names.replace(' ', '').split(',')
  for cname_row in cursor:
    if column_names != '*':
      if cname_row[0] in cnames_to_fetch:
        cnames.append(cname_row[0])
    else:
      cnames.append(cname_row[0])

  cursor.execute(query)
  data = []
  for data_row in cursor:
    drow = {}
    for cname in cnames:
      drow[cname] = data_row[cname]
    data.append(drow)
  return data

def insert(conn, table_name, col_val_dict, pk_name = 'id'):
  col_str = ', '.join(col_val_dict.keys())
  val_placeholder_str = ''
  for col, val in col_val_dict.items():
    if val_placeholder_str == '':
      val_placeholder_str = '%({})s'.format(col)
    else:
      val_placeholder_str += ', %({})s'.format(col)

  query = "INSERT INTO {} ({}) VALUES({})".format(table_name, col_str, val_placeholder_str)
  query = '{} RETURNING {}'.format(query, pk_name)
  cursor = conn.cursor()
  cursor.execute(query, col_val_dict)
  conn.commit()
  new_row_id = cursor.fetchone()[0]
  return new_row_id


def update(conn, table_name, col_val_dict, condition):
  query = "UPDATE {} SET ".format(table_name)
  val_placeholder_str = ''
  for col, val in col_val_dict.items():
    if val_placeholder_str == '':
      val_placeholder_str = '{}=(%s)'.format(col, val)
    else:
      val_placeholder_str += ", {}=(%s)".format(col, val)
  query = query + val_placeholder_str + ' WHERE {}'.format(condition)
  cursor = conn.cursor()

  cursor.execute(query, col_val_dict.values())
  conn.commit()

def delete(conn, table_name, condition):
  query = "DELETE FROM {} WHERE {}".format(table_name, condition)
  cursor = conn.cursor()
  cursor.execute(query)
  conn.commit()



def demo():
  conn = create_connection('testingdb', '127.0.0.1', 'postgres', 'postgres')
  # data = select(conn, 'users', '*', "LIMIT 10")
  # print "\n\nBEFORE INSERT\n\n"
  # print data
  # print "\n\n"
  # new_id = insert(conn, 'users', {'first_name' : 'Sus', 'last_name' : 'vedi'})
  # print new_id
  # print "\n\nAFTER INSERT\n\n"
  # data = select(conn, 'users', 'id, first_name', " ORDER BY first_name LIMIT 10")
  # print data
  # update(conn, 'users', {'first_name' : 'naresh', 'last_name' : 'dwivedi', 'age' : 28}, 'id=1')
  # delete(conn, 'users', 'id=2')
  # conn.close()

#demo()
