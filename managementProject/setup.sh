#!/bin/bash

# Install dependencies
pip install -r requirements.txt

# Additional commands
python manage.py tailwind install
python manage.py makemigrations
python manage.py migrate