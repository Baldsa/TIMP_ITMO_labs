#!/bin/bash


var1='3'
var2='10'
if [ -e /home/balora/.setups1 ]; then
  echo ' ' > /dev/null
else
  mkdir /home/balora/.setups1
  touch /home/balora/.setups1/.files1
  echo "3 
  10" > ~/.setups1/.files1
fi

sudo cp ./lab2.py /usr/bin/lab21.py
sudo chmod 755 /usr/bin/lab21.py
mkdir ~/TIMP/lab2_D1/.namefile || echo "Уже установленно"
touch ~/TIMP/lab2_D1/.namefile/names.json
echo "{\"names\":[]}" | sudo tee ~/TIMP/lab2_D1/.namefile/names.json > /dev/null
