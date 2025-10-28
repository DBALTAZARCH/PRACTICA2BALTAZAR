# kept for compatibility if someone runs it directly
from database import init_db
from flask import Flask
app = Flask(__name__)
app.config.from_object('config.Config')
init_db(app)
print('Database initialized at', app.config['DB_PATH'])
