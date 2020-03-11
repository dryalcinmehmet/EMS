#!/bin/bash


function create_workers() {

docker-machine create -d virtualbox \ --engine-label role=manager \manager



  for ((i=2;i<=4;i++)); do

    docker-machine create --driver virtualbox node$i

    echo Worker $i is created!
done
echo "Finish creating staffs!"
}

function clear() {
      systemctl stop elasticsearch &&
      systemctl stop kibana &&
      systemctl stop logstash &&
      kill -9 $(lsof -t -i:5044) || echo "ok"  &&
      kill -9 $(lsof -t -i:5601) || echo "ok" &&
      kill -9 $(lsof -t -i:9200) || echo "ok" &&
      kill -9 $(lsof -t -i:80) || echo "ok" &&
      kill -9 $(lsof -t -i:8000) || echo "ok" &&
      docker container stop $(docker container ls -aq) || echo "ok" &&
      docker container rm $(docker container ls -aq) || echo "ok" &&
      docker volume prune   || echo "ok" &&
      docker network prune   || echo "ok"
      docker image prune  || echo "ok" &&
      docker image prune -a || echo "ok"
}

function clear_ports() {
      kill -9 $(lsof -t -i:5044) || echo "ok"  &&
      kill -9 $(lsof -t -i:5601) || echo "ok" &&
      kill -9 $(lsof -t -i:9200) || echo "ok" &&
      kill -9 $(lsof -t -i:80) || echo "ok" &&
      kill -9 $(lsof -t -i:8000) || echo "ok" &&
      kill -9 $(lsof -t -i:8080) || echo "ok"
}


function init() {
    docker-compose -f docker-compose.yml down -v &&
    docker-compose -f source/airflow/docker-compose-LocalExecutor.yml down -v &&
    docker-compose -f docker-compose.yml up -d --build &&
    docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput &&
    docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input &&
    docker-compose up -d --no-deps --build web &&
    docker-compose -f source/airflow/docker-compose-LocalExecutor.yml up -d --build
}

function init_justup() {

    docker-compose -f docker-compose.yml up -d --build &&
    docker-compose -f docker-compose.yml exec web python manage.py migrate --noinput &&
    docker-compose -f docker-compose.yml exec web python manage.py collectstatic --no-input&&
    docker-compose up -d --no-deps --build web &&
    docker-compose -f source/airflow/docker-compose-LocalExecutor.yml up -d --build
}


function mysql() {
apt-get install mysql-server &&
apt-get install mysql-server libapache2-mod-auth-mysql &&
service mysql start &&
mysql -u root -p &&
create database test;
show databases;
quit

}
# Check if the function exists (bash specific)
if declare -f "$1" > /dev/null
then
  # call arguments verbatim
  "$@"
else
  # Show a helpful error
  echo "'$1' is not a known function name" >&2
  exit 1
fi
