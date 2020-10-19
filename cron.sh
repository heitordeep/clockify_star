#!/bin/bash

param=$1
ARGS_ALLOWED=1
PATH_FILE=/usr/local/airflow/dags/clockify_star

if [ -z $param ]
    then 
        echo "Você precisa passar $ARGS_ALLOWED paramêtro no shell."

elif [ $# -gt $ARGS_ALLOWED ]
    then
        echo "Você passou $# parametros. Você só pode passar apenas $ARGS_ALLOWED paramêtro."

elif [ $param = "update" ]
    then 
        PROJECT_ID=$(cat $PATH_FILE/job/start_job.json | grep -i projectId | cut -d ':' -f2 | cut -d '"' -f2)
        python $PATH_FILE/clockify_app/get_parameters_api.py get_task $PROJECT_ID
        python $PATH_FILE/clockify_app/get_parameters_api.py get_project
        python $PATH_FILE/clockify_app/get_parameters_api.py get_tags
else 
    python $PATH_FILE/main.py $param
fi


