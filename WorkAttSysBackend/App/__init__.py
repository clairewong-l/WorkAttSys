from flask import Flask
from flask_cors import CORS

from flask_sqlalchemy import SQLAlchemy

from App.setting import DB_URI

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DB_URI
app.config["JSON_AS_ASCII"] = False
CORS(app, supports_credentials=True)
# app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@127.0.0.1:3306/workattsys'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)

