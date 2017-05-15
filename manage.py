from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://sasha:1234@localhost/chess'
app.config['SQLALCHEMT_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
manager = Manager(app)

@app.route('/')
def index():
	return '<h1> Hello </h1>'

if __name__ == '__main__':
	manager.run()
