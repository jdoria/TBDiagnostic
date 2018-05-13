#!/bin/bash
# =======================================================================
#                     Shell Script for deploy Django App
# =======================================================================
echo -e "\n==============================================="
echo     " Modifying the sudoers file"
echo     "==============================================="

sudo echo -e "\nroot ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

echo -e "\n==============================================="
echo     " Installing Git"
echo     "==============================================="
sudo apt-get --yes --force-yes install git

echo -e "\n==============================================="
echo     " Cloning repository"
echo     "==============================================="
mkdir djangoApplication
git clone https://github.com/jdoria/TBDiangostic.git djangoApplication

cd  djangoApplication 
git  checkout development
cd ..

echo -e "\n==============================================="
echo     " Installing PostgreSQL"
echo     "==============================================="
sudo apt-get update
sudo apt-get --yes --force-yes install postgresql postgresql-contrib

# Logging in with PostgreSQL and create database
sudo -u postgres psql -c 'create database TBDiagnostic;'

echo -e "\n==============================================="
echo     " Verifying the installed version of Python"
echo     "==============================================="

current_python_version="$(python3 --version)"
required_python_version="Python 3.5.1"

if [ "$python_version"!="$required_python_version" ]; then
    echo " -- Installing Python version required."
    sudo apt-get install python3.5
else
    echo " -- Python version is not required."
fi

sudo apt-get --yes --force-yes install python-setuptools python-dev build-essential
sudo easy_install pip
sudo apt-get -y install python3-pip
pip install --upgrade pip
pip3 install -r ./requirements.txt
sudo apt-get install python3-psycopg2

python3 ./manage.py makemigrations
python3 ./manage.py migrate
