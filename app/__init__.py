#app/__init__.py
from flask import Flask

app = Flask(__name__)

from app.main.main_routes import main_blueprint
from app.admin.admin_routes import admin_blueprint


app.register_blueprint(main_blueprint)
app.register_blueprint(admin_blueprint, url_prefix='/admin')
