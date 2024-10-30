from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_login import LoginManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb1.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = str(uuid.uuid4())
manager = LoginManager(app)

