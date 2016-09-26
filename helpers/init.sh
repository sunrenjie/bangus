#!/usr/bin/env bash

echo Do it if necessary: python3 ../manage.py makemigrations
mysql -e 'DROP DATABASE bangus;'
mysql -e 'CREATE DATABASE bangus DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;'
python3 ../manage.py migrate
python3 ../manage.py shell < data-population.py
