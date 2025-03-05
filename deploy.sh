#!/bin/bash

echo "Starting deployment..."

# Pull latest changes
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install/update dependencies
pip install -r requirements.txt

# Make sure .env.production is linked
if [ ! -f .env.production ]; then
    ln -s /etc/expense-tracker/.env.production .env.production
fi

# Apply migrations
python3 manage_prod.py migrate

# Collect static files
python3 manage_prod.py collectstatic --noinput

# Restart Gunicorn
sudo systemctl restart gunicorn

echo "Deployment complete!" 
