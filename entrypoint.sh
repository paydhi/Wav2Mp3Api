#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status
set -x  # all executed commands are printed to the terminal.


python manage.py migrate --noinput
python manage.py collectstatic --noinput
python manage.py runserver 0.0.0.0:8000