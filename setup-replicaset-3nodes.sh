#!/bin/bash

# This script is to set up a MongoDB replica set of three members 
# in a cluster of three nodes for Dr. Kim's CS157C NoSQL class.  
# Each replica set member resides in a separate node.

for n in 0 1 2; do
  docker ps -a |grep -q mongodb$n.project.net
  if [ $? -ne 0 ]; then
    echo -e "\n\033[1;31mERROR: 3 containers need to exist and be up first.\033[0m\n"
    echo "$ docker ps -a"
    docker ps -a
    exit 1
  fi
done

docker cp Files-to-copy/setup-replication.sh mongodb0.project.net:/tmp

for n in 0 1 2; do
  docker exec -t mongodb$n.project.net service mongod start
done

sleep 3

docker exec -t mongodb0.project.net /tmp/setup-replication.sh

