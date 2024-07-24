from flask import Flask
from pymongo import MongoClient
from dotenv import load_dotenv
import os

def create_app():
    # Load environment variables from a .env file
    load_dotenv()

    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY=os.getenv('SECRET_KEY', 'default_secret_key'))

    # MongoDB connection setup
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    app.db = client['email_rating_app']

    with app.app_context():
        from . import routes

    return app
