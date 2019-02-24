from flask import Flask
import os

app = Flask(__name__)
#os.path.join(cwd, 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mnt/c/Users/mjsr/code/a_f_p/database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False