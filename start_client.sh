#! /bin/bash
#
# Usage:  ./start.sh [port]
#  
# Start the service as a background process, saving
# the process number (of the lead process) in SERVICE_PID.
#
#

PORTNUM=$1
if [[ "${PORTNUM}" == "" ]]; then
    PORTNUM="8080"
fi;

echo "***Will listen on port ${PORTNUM}***"

# this=${BASH_SOURCE[0]}
# here=`dirname ${this}`
# activate="${here}/env/bin/activate"
# echo "Activating ${activate}"
# source ${activate}
# echo "Activated"

pushd Client
python3 client.py -p ${PORTNUM} > clientLog.txt 2>&1 &
pid=$!
popd
echo "${pid}" >SERVICE_PID
echo "***"
echo "Flask server started"
echo "PID ${pid} listening on port ${PORTNUM}"
echo "SERVICE_PID: " `cat SERVICE_PID`
echo "***"

