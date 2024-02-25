import os

from dotenv import load_dotenv

load_dotenv()

DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_NAME = os.environ.get('DB_NAME')
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')

DB_USER_TEST = os.environ.get('DB_USER_TEST')
DB_PASSWORD_TEST = os.environ.get('DB_PASSWORD_TEST')
DB_NAME_TEST = os.environ.get('DB_NAME_TEST')
DB_HOST_TEST = os.environ.get('DB_HOST_TEST')
DB_PORT_TEST = 5432  # os.environ.get('DB_PORT_TEST')

JWT_SECRET = os.environ.get('JWT_SECRET')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES'))
ALGORITHM = os.environ.get('ALGORITHM')
