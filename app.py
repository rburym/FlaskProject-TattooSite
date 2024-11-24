from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import uuid
from flask_login import LoginManager
from flask_toastr import Toastr

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///testdb1.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = str(uuid.uuid4())
manager = LoginManager(app)
app.config['SECRET_KEY'] = 'bjndfw'
app.config['TOASTR_POSITION_CLASS'] = 'toast-top-left'
toastr = Toastr(app)

