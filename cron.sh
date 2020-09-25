#!/bin/bash

param=$1
ARGS_ALLOWED=1

if [ -z $param ]
    then 
        echo "Você precisa passar 1 paramêtro no shell."

elif [ $# -gt $ARGS_ALLOWED ]
    then
        echo "Você só pode passar $ARGS_ALLOWED paramêtro no comando shell."
else 
    python /usr/local/airflow/clockify/main.py $param
fi


