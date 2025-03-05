#!/bin/bash
# Update system
sudo apt-get update
sudo apt-get -y upgrade

# Install Python and dependencies
sudo apt-get install -y python3-pip python3-dev nginx
sudo apt-get install -y postgresql postgresql-contrib

# Install virtualenv
pip3 install virtualenv

# Create project directory
mkdir -p /home/ubuntu/expense_tracker
cd /home/ubuntu/expense_tracker

# Create virtual environment
virtualenv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Configure Nginx
sudo rm /etc/nginx/sites-enabled/default
sudo touch /etc/nginx/sites-available/expense_tracker 