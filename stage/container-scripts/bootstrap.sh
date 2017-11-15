#!/usr/bin/env bash

#sudo do-release-upgrade
#sudo sed -i '54s/#//' /etc/gai.conf
sudo yum remove docker \
                docker-engine \
                docker-engine-selinux
sudo yum update -y
sudo yum install -y \
    apt-    transport-https \
    ca-certificates \
    curl \
    software-properties-common
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update -y
sudo apt-get install -y docker-ce
sudo sed -i "s/vagrant-ubuntu-trusty-64/$HOSTNAME/g" /etc/hostname
sudo reboot
