#!/bin/bash


# Create Database for user storage
sudo docker network create internmate

# create a sql table
PASSWORD=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 32 | head -n 1)
echo "MYSQL PASSWORD IS: $PASSWORD"
docker run --network internmate --expose 3306 --name internmate_db -e MYSQL_ROOT_PASSWORD=$PASSWORD -d mysql:latest

#print network details

sudo docker network inspect internmate

echo "What is the MYSQL IP?"
read IPADDRESS
echo "We have to wait for few seconds to docker to spin up. Sleeping for 15 seconds. DO NOT QUIT THIS PROGRAM"
sleep 15
mysql -u root -p -h $IPADDRESS < db.sql
echo "Now run the following commands:"
echo "export DB_IP=$IPADDRESS"
echo "export DB_PASS=$PASSWORD"
echo "SECRET_KEY=secret" #this is only for local deployment not for prod.
