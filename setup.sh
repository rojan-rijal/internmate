sudo apt-get install docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $(whoami)
sudo apt-get install -y libmysqlclient-dev && sudo apt-get install mysql-client && sudo apt-get install python3-pip
pip3 install -r requirements.txt
