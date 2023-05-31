#!/bin/bash
# $1 = (number of control planes)
# We will check these additional control planes once every 30s until they are up.
# Once we see the host online, we will add it to the load balancer config.
for (( i=2; i<=$1; i++ ))
do
    until nc -vzw 2 192.168.50.$(($i+10)) 22 >/dev/null 2>&1; do sleep 30; done && \
    python3 /home/vagrant/update-haproxy-cfg.py cp-$i=192.168.50.$(($i+10)) && \
    systemctl restart haproxy &
done