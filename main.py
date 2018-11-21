from modules.psql.psql_get import psql_get
from modules.modbus import rack_modbus
from modules.misc.threadHandling import a_thread
from modules.misc.errors import *
from config.config import color_picker,SLEEP_TIME
from time import sleep

# TASK FOR THREADING
def modbus_execute(loc,col):
	response=rack_modbus.execute(loc,col)
	sleep(SLEEP_TIME) # delay until lamp off
	response+=rack_modbus.execute(loc,'1')
	print(response)
# END TASK FOR THREADING

print(".")

while True:
    try:
        get = psql_get() # capture the first occuring request
        thrd = a_thread() # create a thread
        thrd.run_task(modbus_execute,get['locators'],color_picker(get['user_id']))
        del(thrd,get) # cleaning up the used thread
        
    except KeyboardInterrupt:
        print(".")
        print("Exiting the program....")
        exit()

    except Exception as e: # if error, log them
        error_log("""REQUEST : %s -> ERROR : %s\n""" % (str(get) if 'get' in locals() else '0',str(e)))
        exit()

    else:
        print("DONE!")
        print(".")
        continue
