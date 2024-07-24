from flask import Flask
from pymongo import MongoClient
import os
import dotenv

dotenv.load_dotenv()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(SECRET_KEY='your_secret_key')

    # MongoDB connection setup
    mongo_uri = os.getenv('MONGO_URI')
    client = MongoClient(mongo_uri)
    app.db = client['email_rating_app']

    with app.app_context():
        from . import routes

    return app
