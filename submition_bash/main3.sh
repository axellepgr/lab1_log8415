#!/bin/bash
echo "Installing the following dependencies: boto3 - requests - paramiko"
pip3 install boto3
pip3 install requests
pip3 install paramiko

echo "Clonning the git repo to proceed with the deployment"
#!/bin/bash
echo "Installing the following dependencies: boto3 - requests - paramiko"
pip install boto3
pip install requests
pip install paramiko

echo "Clonning the git repo to proceed with the deployment"
git clone https://github.com/axellepgr/lab1_log8415.git
echo "Some set up"
echo "1-Please make sure you updated .aws/Creadentials"
read -p "Was the previous step completed?(y)" confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
echo "2-Please enter the .pem file of your key pair names 'vockey' in the root folder of lab1_log8415"
read -p "Was the previous step completed?(y)" confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

cd lab1_log8415/tmp
python set_up.py
echo "Some set up"
echo "1-Please make sure you updated .aws/Creadentials"
read -p "Was the previous step completed?(y)" confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1
echo "2-Please enter the .pem file of your key pair names 'vockey' in the root folder of lab1_log8415"
read -p "Was the previous step completed?(y)" confirm && [[ $confirm == [yY] || $confirm == [yY][eE][sS] ]] || exit 1

cd lab1_log8415/tmp
python3 set_up.py
