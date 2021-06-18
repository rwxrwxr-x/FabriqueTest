#!/bin/bash

run() {
  gunicorn fabrique.wsgi:application -w 4 -b 0.0.0.0:8000
}

migrations() {
  python manage.py makemigrations $1
}

migrate() {
  python manage.py migrate
}

debug() {
  python manage.py runserver
}

case $1 in
      run)
        migrations

        migrate "auth"
        migrate "--run-syncdb --no-input"

        if [[ "$DEBUG" == "True" ]]; then
          debug $2
        else
          run $2
        fi
      ;;
      migrations)
        migrations $2
      ;;
      migrate)
        migrate $2
      ;;
      *) echo "Invalid option: $1"
      ;;
esac

exit 0



