#!/bin/sh
#
# Template Jenkins for Freetsyle project > shell script job
# Makes use of common linux shell script commands to parse
## curl,base64,xmlllint,sed,gunzip
## consider using Jenkins parameters in job definition

PENTAHO_RESTAPI_SLEEPTIME=5
# example use of Jenkins defined parameter
# PENTAHO_RESTAPI_SLEEPTIME=$p_retry_interval
FULL_JOB_TO_LAUNCH_PATH="/public/projects/demo/j_run_something_main"
PENTAHO_USER="admin"
PENTAHO_PASS="password"
PENTAHO_HOST="localhost"

id=`curl -sL "http://$PENTAHO_HOST:8080/pentaho/kettle/runJob?job=$FULL_JOB_TO_LAUNCH_PATH" -H "Authorization: Basic \`echo -n $PENTAHO_USER:$PENTAHO_PASS | base64\`" |grep "<id>" |awk -F "[><]" '/id/{print $3}'`
echo $id
date
while :
do 
   jstatus=`curl -sL "http://$PENTAHO_HOST:8080/pentaho/kettle/jobStatus?&id=$id&xml=Y" -H "Authorization: Basic \`echo -n $PENTAHO_USER:$PENTAHO_PASS | base64\`" | xmllint --xpath "string(//status_desc)" - `
   if [ "$jstatus" != "Running" ]
   then
      #curl -sL "http://$PENTAHO_HOST:8080/pentaho/kettle/jobStatus?id=$id&xml=Y" -H "Authorization: Basic `echo -n $PENTAHO_USER:$PENTAHO_PASS | base64`" | xmllint --xpath "string(//logging_string)"  - | sed -e 's|<!\[CDATA\[||g; s|\]\]>||g' | base64 -d | gunzip
      break
   fi
   echo $jstatus
   sleep $PENTAHO_RESTAPI_SLEEPTIME
done
echo $jstatus
date
echo "############ DONE #########"
if [ "$jstatus" = "Finished" ]
then
   echo "Success"
   curl -sL "http://$PENTAHO_HOST:8080/pentaho/kettle/jobStatus?id=$id&xml=Y" -H "Authorization: Basic `echo -n $PENTAHO_USER:$PENTAHO_PASS | base64`" | xmllint --xpath "string(//logging_string)"  - | sed -e 's|<!\[CDATA\[||g; s|\]\]>||g' | base64 -d | gunzip
   exit 0
else
   echo "Failed"
   curl -sL "http://$PENTAHO_HOST:8080/pentaho/kettle/jobStatus?id=$id&xml=Y" -H "Authorization: Basic `echo -n $PENTAHO_USER:$PENTAHO_PASS | base64`" | xmllint --xpath "string(//logging_string)"  - | sed -e 's|<!\[CDATA\[||g; s|\]\]>||g' | base64 -d | gunzip
   exit 1
fi
