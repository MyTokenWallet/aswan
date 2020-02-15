#!/usr/bin/env bash


#mongo:
docker run -d --name mongo -v $HOME/docker_volumes/mongodb:/data/db  -p 27017:27017 mongo:latest
mysql: docker run -d --name mysql -e MYSQL_ROOT_PASSWORD=root -v $HOME/docker_volumes/mysql:/var/lib/mysql -v $HOME/docker_volumes/conf/mysql:/etc/mysql/conf.d -p 3306:3306 mysql:5.6
redis: docker run -d --name redis -p 6379:6379  -v $HOME/docker_volumes/redis:/var/lib/redis redis:latest