sudo docker container stop main-internmate-app
sudo docker container prune
sudo docker build -t rojanrijal/main-internmate-app .
sudo docker run --name main-internmate-app --expose 8000 --network internmate -d rojanrijal/main-internmate-app
