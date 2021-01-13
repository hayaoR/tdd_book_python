Provisioning a new site
=======================

## Required package:

# nginx
# Python 3.6
# virtualenv + pip
# Git

e.g., on Ubuntu:
	
	sudo add-apt-repository ppa:deadsnakes/ppa
	sudo apt update
	sudo apt install nginx git python3.6 python3.6-venv

## Nginx Virtual Host config

* see nginx.template.conf
* replace DOMAIN with, e.g., staging.my-domain.com

## Systemd service

* see gunicorn-systemd.template.service
* replace DOMAIN with, e.g., staging.my-domain.com

## Folder structure

Assume we have a user account at /home/username

/home/username
	site
		Domain1
			.env
			db.sqlite3
			manage.py etc
			static
			virtualenv
		Domain2
			.env
			db.sqlite3
			etc


