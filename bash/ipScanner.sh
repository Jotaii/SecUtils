#!/bin/bash

#TODO: implement version for given a mask show all posible ips.

#this script just works with /24 inet
if [ "$1" == "" ]
then
echo "Missing IP Adress!"
echo "Syntax: ./ipScanner.sh 192.168.4"

else
for ip in `seq 1 254`; do
ping -c 1 $1.$ip | grep "64 bytes" | cut -d " " -f 4 | tr -d ":" &
done
fi
