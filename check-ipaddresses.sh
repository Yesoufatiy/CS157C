#!/bin/bash


c_list=$(docker ps -a|awk '!/NAME/ {print $NF}'|sort -V)

for c in $c_list; do
  c_ip=$(docker inspect $c |awk '/IPv4A/ {gsub("\"", ""); print $2}')
  echo "$c $c_ip"
done

