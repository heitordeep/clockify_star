#!/bin/bash

env=$(pyenv versions)

param=$1
ARGS_ALLOWED=1
name_env="clockify"

eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)"


if [ -z $param ]
    then 
        echo "Você precisa passar 1 paramêtro no shell."

elif [ $# -gt $ARGS_ALLOWED ]
    then
        echo "Você só pode passar $ARGS_ALLOWED paramêtro no comando shell."

else 
    if [ `echo $env | grep -c "$name_env" ` -eq 1 ]
        then
            pyenv activate $name_env
            echo "Env $name_env ativada!"
            make run args=$param
    else
        pyenv virtualenv $name_env
        pyenv activate $name_env
        make requirements
        make run args=$param
    fi
fi


