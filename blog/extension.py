from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

from flask_wtf import CSRFProtect
from combojsonapi.spec import ApiSpecPlugin
from combojsonapi.event import EventPlugin
from combojsonapi.permission import PermissionPlugin

def create_api_spec_plugin(app):
    api_spec_plugin = ApiSpecPlugin(
        app=app,
        tags={
        "Tag": "Tag API",
        "User": "User API",
        "Article": "Article API",
        "Author": "Author API",
        }
    )
    
    return api_spec_plugin

def create_event_plugin(app):
    event_plugin = EventPlugin()        
    
    return event_plugin

def create_permission_plugin(app):
    permission_plugin = PermissionPlugin()        
    
    return permission_plugin


db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
csrf = CSRFProtect()
