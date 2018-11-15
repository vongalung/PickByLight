from os import path
# ROOT DIR
ROOT_DIR = path.abspath(path.join(path.dirname(__file__),'..'))

# DATABASE TABLES
REQ_TAB = 'rpi_request'

# ERROR LOGGING
ERROR_LOG_PATH = path.join(ROOT_DIR,'logs','error.log')
ERROR_LOG_FORMAT = "%(asctime)-15s\n%(message)s"

# MULTI-THREADING CONFIGURATIONS
SLEEP_TIME = 30 # in seconds

# LAMP COLOR PICKER
COLOR_PICKER = {
	'ID1':'R',
	'ID2':'B'
}

