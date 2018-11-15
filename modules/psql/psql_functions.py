# exist function
# 'val' should be written within '...', that is only accepts string value
# set 'condition'=[condition_string] to overwrite the use of 'var'='val'
# the [value] should be ended with "'", and [other_value] should not be ended by "'"
# function return a value of 't' or 'f'
def exist(table,var='0',val='0',condition=None):
    if not condition:
        condition=""" WHERE """+var+"""="""+str(val)
    else:
        condition=""" WHERE """+condition
    que="""SELECT EXISTS (SELECT * FROM """+table+condition+""")"""
    return que
    
# count function
# 'val' should be written within '...', that is only accepts string value
# set 'condition'=[condition_string] to overwrite the use of 'var'='val'
# function returns an integer
def count(table,var='0',val='0',condition=None):
    if not condition:
        condition=""" WHERE """+var+"""="""+str(val)
    else:
        condition=""" WHERE """+condition
    que="""SELECT COUNT(*) FROM """+table+condition
    return que
    
# select function
# 'val' should be written within '...', that is only accepts string value
# set 'distinct'='yes' to perform SELECT DISTINCT...
# set 'condition'=[condition_string] to overwrite the use of 'var'='val'
# 'rows'=[integer] specifies how many rows should be selected
# 'order'=[column_name] specifies which column should be a basis for sorting
# function returns a tuple of format specified by  'split'
def select(table,column='*',var='0',val='0',distinct='no',rows=None,order=None,condition=None):
    if distinct=='yes':
        distinct=' DISTINCT'
    elif distinct=='no':
        distinct=""
    if not rows:
        rows=""
    else:
        rows=""" FETCH FIRST """+str(rows)+""" ROWS ONLY"""
    if not order:
        order=""
    else:
        order=" ORDER BY "+order
    if not condition:
        condition=""" WHERE """+var+"""="""+str(val)
    else:
        condition=""" WHERE """+condition
    que="""SELECT"""+distinct+""" """+column+""" FROM """+table+condition+order+rows
    return que
    
# delete one/several row satisfying given condition 'var'='val'.
# 'val' should be written within '...', that is only accepts string value
# set 'condition'=[condition_string] to overwrite the use of 'var'='val'
# 'limit'=[integer] specifies how many rows (max) should be removed at a time
# 'order'=[column_name] specifies which column should be a basis for sorting
# function returns None
def delete(table,var='0',val='0',limit=None,order=None,condition=None):
    lim_front=""
    lim_back=""
    order_by=""
    if not condition:
        condition=""" WHERE """+var+"""="""+str(val)
    else:
        condition=""" WHERE """+condition
    if limit:
        lim_front=""" WHERE ctid IN (SELECT ctid FROM """+table
        lim_back=""" LIMIT """+str(limit)+""")"""
        if order:
            order_by=""" ORDER BY """+order
    que="""DELETE FROM """+table+lim_front+condition+order_by+lim_back
    return que

# insert values into their respective columns.
# 'column' is a 1-D list, consisting of column names,
#     column[column_number]
# 'values' is a tuple of values to be inserted into columns,
#     values[row_number][column_number]
# function returns None
def insert(table,column,values):
    col_str=""
    val_str=""
    for col in column:
        col_str=col_str+col+""","""
    col_str=col_str[:len(col_str)-1]
    for i in range(len(values)):
        val_str+="""("""
        for val in values[i]:
            val_str+="""\'"""+str(val)+"""\',"""
        val_str=val_str[:len(val_str)-1]
        val_str+="""),"""
    val_str=val_str[:len(val_str)-1]
    que="""INSERT INTO """+table+""" ("""+col_str+""") VALUES """+val_str
    return que

# update content(s) of a table satisfying given condition 'var'='val'.
# 'val' should be written within '...', that is only accepts string value
# set 'condition'=[condition_string] to overwrite the use of 'var'='val'
# 'update' is a list (tuple) of column,value pair,
#     [[col1,val1],[col2,val2],[col3,val3],...]
# function returns None
def update(table,update,var='0',val='0',condition=None):
    upd_pairs=""
    if not condition:
        condition=""" WHERE """+var+"""="""+str(val)
    else:
        condition=""" WHERE """+condition
    for set in update:
        upd_pairs+=set[0]+"""=\'"""+str(set[1])+"""\',"""
    upd_pairs=upd_pairs[:len(upd_pairs)-1]
    que="""UPDATE """+table+""" SET """+upd_pairs+condition
    return que

def split_col(dum):
    row=len(dum)
    col=len(dum[0])
    ddum=[[None]]*col
    for i in range(col):
        dddum=[None]*row
        for j in range(row):
            dddum[j]=dum[j][i]
        ddum[i]=dddum
    return ddum

# FOR DEBUGGING ONLY
if __name__ == '__main__':
    upd_list=[['bar_code',999],['c_locator_id',"""13000   """]]
    con_var='c_locator_id'
    con_val="""\'\'"""
    que=update('rpi_ongoing',upd_list,var=con_var,val=con_val)
    print(que)
