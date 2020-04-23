#!/bin/bash


# Create Database for user storage
sudo docker network create internmate
docker container stop internmate_db
docker container stop chat_mongo
docker container prune
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
echo "Updating main db."
mysql -u root -p -h $IPADDRESS < db.sql

echo "Deploying Chat Database next. The password is still the same. Username is: chat_admin"
docker run -d --network internmate --name chat_mongo -e MONGO_INITDB_ROOT_USERNAME=chat_admin -e MONGO_INITDB_ROOT_PASSWORD=$PASSWORD -e MONGO_INITDB_DATABASE=chatdb mongo
echo "Now run the following commands:"
echo "export DB_IP=$IPADDRESS"
echo "export DB_PASS=$PASSWORD"
echo "export SECRET_KEY=secret" 
echo "export CHAT_PASS=$PASSWORD"
echo "export CHAT_IP=IP"
echo "Once done, go to intern_app/ and run python3 run.py"
