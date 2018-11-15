import psql_connection
from config.config import REQ_TAB

conn=psql_connection.connection()

# keep looping indefinitely until an input is found in rpi_request
def psql_avail():
    dum=[]
    while (len(dum)==0):
        dum=conn.select(REQ_TAB,column="req_id,locators,TRIM(user_id) as user_id",order="req_time ASC")
    return dum[0]

# remove read request so that next requests may be executed.
# in the event of duplicate requests, delete them along
def psql_rem(req_id):
    conn.delete(REQ_TAB,var='req_id',val=req_id)

# get the first entry of REQ_TAB
def psql_get():
    row=psql_avail()
    psql_rem(row['req_id'])
    row['locators'] = row['locators'].split(';')

    return row # [req_id,list_of_locators,color]

# FOR DEBUGGING PURPOSE ONLY
if __name__ == '__main__':
    data = psql_get()
    print(data)
