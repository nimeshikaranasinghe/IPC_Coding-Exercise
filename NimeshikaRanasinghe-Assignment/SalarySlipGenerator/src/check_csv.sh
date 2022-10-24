#!/bin/bash

DIR_PATH="$1"
NAME="$2"
LAST_DATE=`date -d "$(date +%Y-%m-01) -1 day" +%Y%m%d`
FILE="${DIR_PATH}${NAME}_${LAST_DATE}.csv"

if [ ! -f "$FILE" ];
then
    echo "File $FILE does not exist. Your Salary will not we calculated. Please contact your admin"
fi
