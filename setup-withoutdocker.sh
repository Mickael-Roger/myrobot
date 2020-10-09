#!/bin/bash

wget -O - "https://packagecloud.io/rabbitmq/rabbitmq-server/gpgkey" | sudo apt-key add -


sudo tee /etc/apt/sources.list.d/bintray.rabbitmq.list <<EOF
deb https://dl.bintray.com/rabbitmq-erlang/debian bionic erlang
deb https://dl.bintray.com/rabbitmq/debian bionic main
EOF

sudo apt update

sudo apt install -y rabbitmq-server

sudo apt install -y python3-pip

sudo rabbitmqctl add_user 'robot' '2a55f70a841f18b97c3a7db939b7adc9e34a0f1b'
sudo rabbitmqctl set_permissions 'robot' ".*" ".*" ".*"
sudo rabbitmqctl delete_user 'guest' || true

sudo rabbitmq-plugins enable rabbitmq_mqtt rabbitmq_web_mqtt

sudo pip3 install -r robot/src/requirements.txt

sudo mkdir /app/
sudo cp robot/src/* /app/

for i in camera motors robot
do
sudo systemctl stop $i
export ROBOT_SVC=$i
cat pythonsvc.tpl | envsubst > $i.service
sudo mv $i.service /etc/systemd/system/ 
sudo systemctl daemon-reload
sudo systemctl enable $i
sudo systemctl start $i
done


