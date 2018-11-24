#!/bin/bash
BASE_DIR=$(dirname "$0")
LOGFILE="${BASE_DIR}/logs/system.log"

coproc errorHandling {
        ( bash -c 'while read line; do echo $(date): ${line}; done' 1>>$LOGFILE )
}

exec 2>&${errorHandling[1]}

script="${BASE_DIR}/main.py"
source "${BASE_DIR}/bin/activate" &
python $script &

exit 0
