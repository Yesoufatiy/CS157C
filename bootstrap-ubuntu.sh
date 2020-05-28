#!/bin/bash
# This script is to customize the Ubuntu Docker image with necessary 
# packages and configurations for Dr. S. Kim's CS157C NoSQL class. 
# 1. Download Ubuntu:18.04 image from Docker Hub(https:hub.docker.com)
# 2. Install necessary packages including MongoDB into the custom image.
# 3. Copy necessary scripts into the custom image.
# 4. Configure the Docker network.


which docker || (echo "docker does not exist"; exit 1)

cat > Dockerfile <<EOF
FROM ubuntu:18.04
RUN apt-get update \
 && apt-get install -y \
    apt-utils vim wamerican iputils-ping \
    iproute2 telnet wget curl tree sudo \
    git gnupg wget python3 python3-pip \
 && apt-get clean \
 && pip3 install pymongo \
 && wget https://www.mongodb.org/static/pgp/server-4.2.asc > /dev/null 2>&1 \
 && apt-key add server-4.2.asc \
 && echo "deb [ arch=amd64 ] https://repo.mongodb.org/apt/ubuntu bionic/mongodb-org/4.2 multiverse" > /etc/apt/sources.list.d/mongodb-org-4.2.list \
 && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
 && echo $TZ > /etc/timezone \
 && export TZ=US/Pacific \
 && apt-get update \
 && apt-get install -y mongodb-org \
 && apt-get clean
COPY Files-to-copy/* /tmp/copied/
RUN tr -d '\015' < /tmp/copied/service-script-mongod > /etc/init.d/mongod \
 && tr -d '\015' < /tmp/copied/mongod.conf > /etc/mongod.conf \
 && rm -fr /tmp/copied \
 && chmod 755 /etc/init.d/mongod \
 && update-rc.d mongod defaults \
 && mkdir -p /data/db
EOF

docker build -t "myimage:Dockerfile" .

docker network ls |grep mycluster > /dev/null || \
docker network create --subnet 192.168.10.0/24 --ip-range 192.168.10.0/24 mycluster

rm -f Dockerfile
