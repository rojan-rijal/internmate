sudo docker container stop chat_service
sudo docker container prune
sudo docker build -t internmate/chat_service .
sudo docker run --name chat_service --expose 80 --network internmate -d internmate/chat_service
sudo docker container ps
