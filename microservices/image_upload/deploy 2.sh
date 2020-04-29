sudo docker container stop image_upload
sudo docker container prune
sudo docker build -t internmate/image_service .
sudo docker run --name foursquare --network internmate -d internmate/image_service
sudo docker container ps
