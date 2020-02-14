#!/usr/bin/env bash

cur_dir=`pwd`

## Start-up management background (debug, not for production)
nohup python ${cur_dir}/www/manage.py runserver &

# Start the background with uwsgi
#command="uwsgi --master --vacuum --processes 10 --socket 127.0.0.1:8000 --chdir ${cur_dir}/www --max-requests 5000 --module wsgi:application --logto ${cur_dir}/www/risk-control.log --pidfile ${cur_dir}/www/risk-control.pid"
#nohup $command &

# Start the blocklog persistence process
nohup python ${cur_dir}/www/manage.py persistence_hit_log &

## Start Momo control services
nohup python ${cur_dir}/risk_server.py &

