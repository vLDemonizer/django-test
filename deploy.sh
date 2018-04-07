#!/bin/bash

if [ -z $1 ]; then
    echo "Must pass docker-compose file to use"
    exit 1
fi

# Build containers
git pull

docker build -t visualize:app -f Dockerfile .

cd docker/db

docker build -t visualize:db -f Dockerfile .

cd ../..

docker-compose -f $1 down
docker-compose -f $1 up -d
docker-compose -f $1 logs -f