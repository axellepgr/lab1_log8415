#!/bin/bash
read -p "Do you use the commands python3/pip3 instead of python/pip? (y/n): " y
if [ $y == "y" ]
then
    echo "Installing the following dependencies: boto3 - requests - paramiko"
    pip3 install boto3==1.24.89
    pip3 install botocore==1.27.89
    pip3 install paramiko==2.11.0
    pip3 install requests==2.22.0

    echo "Clonning the git repo to proceed with the deployment"
    git clone https://github.com/axellepgr/lab1_log8415.git
    echo "Some set up"
    echo "1-Please make sure you updated .aws/Creadentials"
    read -p "Was the previous step completed?(y)" confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
    echo "2-Please enter the .pem file of your key pair named 'vockey' in the root folder of lab1_log8415/src"
    read -p "Was the previous step completed?(y)" confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

    cd lab1_log8415/src
    python3 launch.py
else
    echo "Installing the following dependencies: boto3 - requests - paramiko"
    pip install boto3==1.24.89
    pip install botocore==1.27.89
    pip install paramiko==2.11.0
    pip install requests==2.22.0

    echo "Clonning the git repo to proceed with the deployment"
    git clone https://github.com/axellepgr/lab1_log8415.git
    echo "Some set up"
    echo "1-Please make sure you updated .aws/Creadentials"
    read -p "Was the previous step completed?(y)" confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
    echo "2-Please enter the .pem file of your key pair named 'vockey' in the root folder of lab1_log8415/src"
    read -p "Was the previous step completed?(y)" confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

    cd lab1_log8415/src
    python launch.py
fi