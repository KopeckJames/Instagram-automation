import os
from dotenv import load_dotenv

def load_credentials():
    load_dotenv()
    username = os.getenv('INSTAGRAM_USERNAME')
    password = os.getenv('INSTAGRAM_PASSWORD')
    client_id = os.getenv('INSTAGRAM_CLIENT_ID')
    client_secret = os.getenv('INSTAGRAM_CLIENT_SECRET')

    return username, password, client_id, client_secret