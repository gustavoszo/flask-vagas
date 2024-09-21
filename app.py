from flask import Flask
from sql_alchemy import banco
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

import os
from dotenv import load_dotenv
load_dotenv()

db_host = os.getenv('DB_HOST')
db_username = os.getenv('DB_USERNAME')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')

app = Flask(__name__)
loginManager = LoginManager()

app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{db_username}:{db_password}@{db_host}/{db_name}'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

banco.init_app(app)
bcrypt= Bcrypt(app)
loginManager.init_app(app)
loginManager.login_view = 'login'
loginManager.login_message = 'Faça o login'
loginManager.login_message_category = 'info'

mail_settings = {
  'MAIL_SERVER': 'smtp.gmail.com',
  'MAIL_PORT': 465,
  'MAIL_USE_TLS': False,
  'MAIL_USE_SSL': True,
  'MAIL_USERNAME': os.getenv('EMAIL'),
  'MAIL_PASSWORD': os.getenv('SENHA')
}

app.config.update(mail_settings)
mail = Mail(app)

from routes import *

if __name__ == '__main__':
  app.run(debug=True) 