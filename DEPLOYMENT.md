# Expense Tracker Deployment Documentation

## System Architecture
- Web Server: Nginx
- Application Server: Gunicorn
- Database: PostgreSQL (AWS RDS)
- Static Files: AWS S3
- Domain: chiwismo.com

## File Structure
/home/ubuntu/expense-tracker/
├── manage.py              # Local development
├── manage_prod.py         # Production management
├── deploy.sh             # Deployment script
├── requirements.txt      # Dependencies
├── expense_tracker/      # Django project
└── expenses/            # Django app

/etc/expense-tracker/
├── .env.production       # Production env vars
└── expense-tracker-key.pem  # SSH key

## Environment Files

### Local Development (.env)
DEBUG=True
DB_NAME=expense_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

### Production (.env.production)
DEBUG=False
DB_NAME=expense_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=your-rds-endpoint
DB_PORT=5432
AWS_ACCESS_KEY_ID=your_key
AWS_SECRET_ACCESS_KEY=your_secret
AWS_STORAGE_BUCKET_NAME=your_bucket

## Deployment Process

### 1. Local Development
# Activate virtual environment
source venv/bin/activate

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Test changes
python manage.py runserver

### 2. Git Deployment
# Commit changes
git add .
git commit -m "Your changes"
git push origin main

### 3. Server Deployment
# SSH into server
ssh -i /path/to/key.pem ubuntu@chiwismo.com

# Run deployment script
cd ~/expense-tracker
./deploy.sh

### 4. Verify Deployment
- Check website: https://chiwismo.com
- Check logs:
  tail -f /var/log/nginx/error.log
  tail -f /var/log/gunicorn/error.log
  tail -f /var/log/django/debug.log

## Service Management

### Nginx
sudo systemctl status nginx
sudo systemctl restart nginx
sudo nginx -t  # Test configuration

### Gunicorn
sudo systemctl status gunicorn
sudo systemctl restart gunicorn

## Troubleshooting

### Common Issues

1. 502 Bad Gateway
# Check Gunicorn socket
ls -l /run/gunicorn/gunicorn.sock

# Check Gunicorn logs
tail -f /var/log/gunicorn/error.log

2. Static Files Missing
# Collect static files
python3 manage_prod.py collectstatic

# Check S3 bucket
aws s3 ls s3://expense-tracker-static-files-pv-2024

3. Database Connection Issues
# Test database connection
psql -h your-rds-endpoint -U postgres -d expense_db

## Security Notes

1. Environment Variables
- Keep .env.production in /etc/expense-tracker/
- Set proper permissions: chmod 600
- Never commit to Git

2. SSL/HTTPS
- Certificates managed by Let's Encrypt
- Auto-renewal configured
- Force HTTPS redirect enabled

3. AWS Credentials
- Use IAM roles when possible
- Regularly rotate access keys
- Limit permissions to required services

## Backup Process

1. Database Backup
pg_dump -h your-rds-endpoint -U postgres expense_db > backup.sql

2. Environment Files
sudo cp /etc/expense-tracker/.env.production /etc/expense-tracker/backups/

## Monitoring

1. Check Application Status
sudo systemctl status nginx gunicorn

2. View Logs
tail -f /var/log/nginx/error.log
tail -f /var/log/gunicorn/error.log
tail -f /var/log/django/debug.log

## Contact

For issues or questions:
- Developer: Pablo Vergara
- Email: pavergaraflores@gmail.com 