from dotenv import load_dotenv
import os

load_dotenv()

# Database environment
DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_USER = os.environ.get('DB_USER')
DB_NAME = os.environ.get('DB_NAME')
DB_PASS = os.environ.get('DB_PASS')

# Bot environment
TOKEN = os.environ.get('TOKEN')

# Youkassa environment
YOUKASSA = os.environ.get('YOUKASSA')

# admins id
admins_id = [int(os.environ.get('ADMIN_ID'))]
