from flask import Flask
from pymongo import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

def create_app():
    # Load environment variables from a .env file
    load_dotenv()

    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY=os.getenv('SECRET_KEY', 'default_secret_key'))

    # MongoDB connection setup
    mongo_uri = os.getenv('MONGO_URI')
    print(f"Connecting to MongoDB with URI: {mongo_uri}")
    client = MongoClient(mongo_uri, server_api=ServerApi('1'))
    app.db = client['email-rewriter']

    with app.app_context():
        from . import routes

    return app
