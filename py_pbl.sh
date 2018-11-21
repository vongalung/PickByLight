#!/bin/sh
ROOT=$(pwd)
PATH="${ROOT}/bin/:{$PATH}"
script='${ROOT}/main.py'
python $script &
exit 0
