from os import path
# ROOT DIR
ROOT_DIR = path.abspath(path.join(path.dirname(__file__),'..'))

# DATABASE TABLES
REQ_TAB = 'rack_automations'

# ERROR LOGGING
ERROR_LOG_PATH = path.join(ROOT_DIR,'logs','error.log')
ERROR_LOG_FORMAT = "%(asctime)-15s\n%(message)s"

# MULTI-THREADING CONFIGURATIONS
SLEEP_TIME = 30 # in seconds

# LAMP COLOR PICKER
GROUP_COLOR_MAP = {
	'ID1':'R',
	'ID2':'B'
}
def color_picker(group_id) :
	if group_id in GROUP_COLOR_MAP :
		return GROUP_COLOR_MAP[group_id]
	else :
		return 'W'
