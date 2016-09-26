#!/usr/bin/env bash

mysql -e 'DROP DATABASE bangus;'
mysql -e 'CREATE DATABASE bangus DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;'
python3 ../manage.py migrate
