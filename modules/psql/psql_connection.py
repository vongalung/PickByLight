import psycopg2
import psycopg2.extras

# CONNECTION OBJECT INITIALIZATION
class connection(object):
	# create connection object based on parameters in
	# a specified file in the same directory
	# (or subdirectory) (default file='config')
	def __init__(self):
		from config.database import *
		self.params(DB_NAME,DB_USER,DB_PASSWORD,DB_HOST,DB_PORT)
	
	# define connection parameters
	def params(self,dbname,username,password=None,host='localhost',port=5432):
		self.host=str(host)
		self.dbname=str(dbname)
		self.port=str(port)
		self.username=str(username)
		self.password=str(password)
	
	# query and output management.
	# in the event of complex queries, use this function instead of
	# the built in functions below!
	# function returns tuple of tup[row][col]
	def query(self,que):
		conn_str = "host="+self.host+" dbname="+self.dbname+" port="+self.port+" user="+self.username+" password="+self.password
		with psycopg2.connect(conn_str) as conn:
			with conn.cursor(cursor_factory = psycopg2.extras.DictCursor) as cursor:
				cursor.execute(que)
				if cursor.description is None:
					rows=None
				else:
					rows=cursor.fetchall()
		conn.commit()
		conn.close()
		return rows
	
	# exist function
	# 'val' should be written within '...', that is only accepts string value
	# set val="""[value] AND [other_var]=[other_value]""" to give multiple conditions
	# the [value] should be ended with "'", and [other_value] should not be ended by "'"
	# function return a value of 't' or 'f'
	def exist(self,table,var='0',val='0',condition=None):
		from modules.psql.psql_functions import exist
		que=exist(table,var,val,condition)
		dum=self.query(que)
		return dum[0]['exists']
	
	# count function
	# 'val' should be written within '...', that is only accepts string value
	# set val="""[value] AND [other_var]=[other_value]""" to give multiple conditions
	# function returns an integer
	def count(self,table,var='0',val='0',condition=None):
		from modules.psql.psql_functions import count
		que=count(table,var,val,condition)
		dum=self.query(que)
		return dum[0]['count']
	
	# select function
	# 'val' should be written within '...', that is only accepts string value
	# set 'distinct'='yes' to perform SELECT DISTINCT...
	# set 'val'="""[condition_1_val] AND [condition_2]""" to give multiple conditions
	# 'rows'=[integer] specifies how many rows should be selected
	# 'order'=[column_name] specifies which column should be a basis for sorting
	# 'split'=['rows'/'column'] switches the tuple output to be either tup[row][col] or tup[col][row]
	# function returns a tuple of format specified by  'split'
	def select(self,table,column='*',var='0',val='0',distinct='no',rows=None,order=None,split='row',condition=None):
		from modules.psql.psql_functions import select
		que=select(table,column,var,val,distinct,rows,order,condition)
		dum=self.query(que)
		if split=='row':
			return dum
		elif split=='column':
			from psql_connection_modules import split_col
			result=split_col(dum)
			return result
	
	# delete one/several row satisfying given condition 'var'='val'.
	# 'val' should be written within '...', that is only accepts string value
	# set 'val'"""[condition_1_val] AND [condition_2]""" to give multiple conditions
	# 'limit'=[integer] specifies how many rows (max) should be removed at a time
	# 'order'=[column_name] specifies which column should be a basis for sorting
	# function returns None
	def delete(self,table,var='0',val='0',limit=None,order=None,condition=None):
		from modules.psql.psql_functions import delete
		que=delete(table,var,val,limit,order,condition)
		dum=self.query(que)
	
	# insert values into their respective columns.
	# 'column' is a 1-D list, consisting of column names,
	#     column[column_number]
	# 'values' is a tuple of values to be inserted into columns,
	#     values[row_number][column_number]
	# function returns None
	def insert(self,table,column,values):
		from modules.psql.psql_functions import insert
		que=insert(table,column,values)
		dum=self.query(que)
	
	# update content(s) of a table satisfying given condition 'var'='val'.
	# 'val' should be written within '...', that is only accepts string value
	# set 'val'"""[condition_1_val] AND [condition_2]""" to give multiple conditions
	# 'update' is a list (tuple) of column,value pair,
	#     [[col1,val1],[col2,val2],[col3,val3],...]
	# function returns None
	def update(self,table,upd,var='0',val='0',condition=None):
		from modules.psql.psql_functions import update
		que=update(table,upd,var,val,condition)
		dum=self.query(que)
	
	# display connection config status
	def status(self):
		for key,value in vars(self).items():
			print("""%s => %s""" % (key,str(value)))
        
# END CONNECTION OBJECT INITIALIZATION

# test program (debug)
if __name__ == '__main__':
	conn=connection()
	tab='material_receive_new'
	col="""poreference,c_locator_id"""
	var="""NOT c_locator_id"""
	val="""\'Z.0\'"""
	po,loc=conn.select(tab,col,var=var,val=val,distinct='yes',split='column')
	print("po\t\t\tloc")
	print("----------------------------------")
	for i in range(len(po)):
		print(po[i]+"\t"+loc[i])
	
