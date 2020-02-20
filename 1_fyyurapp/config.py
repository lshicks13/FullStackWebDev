import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
db_type = 'postgresql'
username = 'postgres'
password = 'secret123'
server = 'localhost'
port = '5432'
db_name = 'fyyurapp'

# TODO IMPLEMENT DATABASE URL
SQLALCHEMY_DATABASE_URI = f'{db_type}://' \
                                        f'{username}:{password}@' \
                                        f'{server}:{port}/' \
                                        f'{db_name}'
