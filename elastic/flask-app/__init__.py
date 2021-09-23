from flask import Flask
from config import Config
from flask_restplus import Api
from elasticsearch import Elasticsearch

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
        if app.config['ELASTICSEARCH_URL'] else None


from application import routes
