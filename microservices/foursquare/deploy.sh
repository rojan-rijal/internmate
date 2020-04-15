sudo docker container stop foursquare
sudo docker container prune
sudo docker build -t internmate/foursquare_service .
sudo docker run --name foursquare --network internmate -d internmate/foursquare_service
sudo docker container ps
