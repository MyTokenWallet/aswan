#!/usr/bin/env bash

# USE THIS FUNCTIONS JUST TO FIX YOUR PY-SYSTEM
#pip check
#target_requirements=requirements-dev.txt
#pip install -U -r $target_requirements
#pip check
#pip freeze > requirements.txt
#deactivate rmvirtualenv pynwb-requirements

## update phyton packages
#sudo -s -H pip3 install PyInstaller -U
#sudo -s -H pip3 list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1  | xargs -n1 pip3 install --upgrade
# cur_dir=`pwd` && python3 ${cur_dir}/www/manage.py runserver & python3 ${cur_dir}/www/manage.py persistence_hit_log & python3 ${cur_dir}/risk_server.py
# REGULAR START
cur_dir=`pwd`
echo . > nohup.out
pip install -r requirements.txt

django-admin makemessages -a
django-admin compilemessages #The SECRET_KEY setting must not be empty.

## Start-up management background (debug, not for production)
nohup python3 ${cur_dir}/www/manage.py runserver &

# Start the background with uwsgi
#command="uwsgi --master --vacuum --processes 10 --socket 127.0.0.1:8000 --chdir ${cur_dir}/www --max-requests 5000 --module wsgi:application --logto ${cur_dir}/www/risk-control.log --pidfile ${cur_dir}/www/risk-control.pid"
#nohup $command &

# Start the blocklog persistence process
nohup python3 ${cur_dir}/www/manage.py persistence_hit_log &

## Start Momo control services
nohup python3 ${cur_dir}/risk_server.py &

