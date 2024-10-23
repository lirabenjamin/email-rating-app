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

    try:
        mongo_uri = os.getenv('MONGO_URI')
        print(f"Connecting to MongoDB with URI: {mongo_uri}")
        client = MongoClient(mongo_uri, server_api=ServerApi('1'))
        app.db = client['ratings']
    except Exception as e:
        logging.error(f"Failed to connect to MongoDB: {e}")
        raise SystemExit("Error: Unable to connect to MongoDB.")
    
    # Customize Jinja2 environment to include enumerate
    app.jinja_env.globals.update(enumerate=enumerate)


    with app.app_context():
        from . import routes

    return app
