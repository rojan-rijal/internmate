import os


SECRET_KEY = os.environ.get('SECRET_KEY') #for CSRF and session cookies creation
SQLALCHEMY_DATABASE_URI = 'mysql://root:{password}@{ip}/internmate'.format(password = os.environ.get('DB_PASS'), ip = os.environ.get('DB_IP')) # SQL Connector for the main app
