from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.heroku import Heroku

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/reddit'
heroku = Heroku(app)
db = SQLAlchemy(app)

class Topic(db.Model):
	__tablename__ = "topics"
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(255))
	n_upvotes = db.Column(db.Integer, default=0)
	n_downvotes = db.Column(db.Integer, default=0)

@app.route("/")
def main():
    return 'Hello World !'

if __name__ == '__main__':
    app.debug = True
    app.run()
