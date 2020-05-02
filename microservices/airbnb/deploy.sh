sudo docker container stop ab
sudo docker container prune
sudo docker build -t internmate/ab_service .
sudo docker run --name ab --network internmate -d internmate/ab_service
sudo docker container ps
