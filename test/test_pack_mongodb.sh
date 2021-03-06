#!/usr/bin/env bash

# Load common shell functions
MYDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
. $MYDIR/common_shell_functions.sh



# Start mongodb
nohup mongod -f /etc/mongod.conf &

/etc/init.d/opsbro start


test/assert_group.sh "mongodb"
if [ $? != 0 ]; then
    echo "ERROR: Mongodb group is not set"
    exit 2
fi

# Wait until the collector is ready
opsbro collectors wait-ok mongodb
if [ $? != 0 ]; then
    echo "ERROR: Mongodb collector is not responding"
    exit 2
fi

RES=$(opsbro evaluator eval "{{collector.mongodb.available}}==True" | tail -n 1)

if [ $RES != "True" ]; then
    echo "Fail: mongodb collectors is not running $RES"
    opsbro collectors show mongodb
    exit 2
fi

opsbro collectors show mongodb

exit_if_no_crash "Mongodb is OK"


