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

mysql -u root -p -h $IPADDRESS < db.sql
