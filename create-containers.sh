#!/bin/bash
# This script is to create Docker containers (by default 3 containers) 
# for Dr. S. Kim's CS157C NoSQL class.
# A static hostname and an IP address are assigned to each container. 
# Usage example: ./create-containers.sh 10 (to create 10 containers)
# Usage example: ./create-containers.sh    (to create 3 containers by default)


max=100

docker network ls |grep -q mycluster || \
docker network create --subnet 192.168.10.0/24 --ip-range 192.168.10.0/24 mycluster

create_container() {
  docker run -td --name mongodb$1.project.net -h mongodb$1.project.net --net mycluster --ip 192.168.10.1$2 -p 27$117:27$117 myimage:Dockerfile
}

if [ $# -eq 1 ]; then
  node_qty=$1
  if [[ $node_qty -gt 0 && $node_qty -lt $max ]]; then
    for nn in $(seq -f "%02g" 0 $node_qty); do
      if [ $nn -lt 10 ]; then
        n=${nn#0}
      fi
      create_container $n $nn
    done
  else
    echo -e "\n\033[1;31mUsage: $0 N where 0 < N < $max\033[0m\n"
    exit 1
  fi
else
  for n in 0 1 2; do
    nn="0$n"
    docker ps -a |grep -q mongodb$n.project.net ||create_container $n $nn
  done
fi

echo ""
./check-ipaddresses.sh


