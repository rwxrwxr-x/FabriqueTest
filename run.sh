#!/bin/zsh
APP='fabrique'
DB='{APP}_postgres'
DB_NAME='{APP}'



_postgres () {
    if [[ $# -le 3 ]];then; echo "Arguments required: name, user, \
    password, db_name";exit 2
    else;echo "Try start container..."
    fi
    response=$(docker run --rm --detach --name=$1 \
        --env POSTGRES_USER=$2 \
        --env POSTGRES_PASSWORD=$3 \
        --env POSTGRES_DB=$4\
        --publish 5432:5432 postgres>/dev/null)
    [[ -z $response ]] || exit 2
}


postgres (){
    : run database
    if [ "$1" = "stop" ]; then
        docker stop $DB | echo '$DB stopped'
        return
    fi
    docker stop $DB || true
    _postgres $DB postgres 123 $DB_NAME
}

app (){
    : run application
    if [ "$1" = "stop" ]; then
        docker stop $APP | echo '$APP stopped'
        return
    fi
    docker stop $APP || true
    docker build -t ${APP}:latest .
    docker run --rm --detach --name=$APP --publish 8000:8003 \
        ${APP}:latest run head
}

migrate (){
  : Finding and applying migrations
  python manage.py makemigrations
  python manage.py migrate
  poetry shell
}

-x (){
    : Running inner cli commands
    python manage.py $@
}


if [ -z $1 ]; then
    typeset -f | grep -w '()' -A1 | grep -v "^--" |
    sed 's/[(){}]//g' | sed 's/[[:space:]]*:[[:space:]]*/:/g' |
    sed 'N;s/\n/ /' | awk '!/help|_/ {print $0}'
    exit 0
fi

export APP_ENV='.env'

poetry shell
"$@"