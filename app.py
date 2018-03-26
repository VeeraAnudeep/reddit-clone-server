import os
from flask import Flask, render_template, request, jsonify, abort
from flask_heroku import Heroku
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/reddit'
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
from datetime import datetime

db = SQLAlchemy()


class BaseModel(db.Model):
    #Base data model for all objects
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        #Define a base way to print models
        # return '%s(%s)' % (self.__class__.__name__, {
        #     column: value
        #     for column, value in self._to_dict().items()
        # })
        return '<id {}>'.format(self.id)

    def json(self):
        #  Define a base way to jsonify models
        return {
            column: value #if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }

#Model for Topics 
class Topics(BaseModel,db.Model):
	__tablename__ = "topics"
	id = db.Column(db.Integer, primary_key=True)
	content = db.Column(db.String(255), nullable=False)
	n_upvotes = db.Column(db.Integer, default=0)
	n_downvotes = db.Column(db.Integer, default=0)
	created_on = db.Column(db.DateTime, nullable=False, default= datetime.utcnow)

	def _to_dict(self):
		return {
			"id" : self.id,
			"content" : self.content,
			"n_upvotes": self.n_upvotes,
			"n_downvotes": self.n_downvotes
		}

@app.route("/")
def main():
    return 'Hello World !'

@app.route("/add-topic/", methods= ['POST'])
def add_topic():
	""""Adds a topic"""
	error = None
	if request.method == 'POST':
		content = request.form['content']
		if not content:
			return "content cannot be Empty"
		topic = Topics()
		topic.content = content
		db.session.add(topic)
		db.session.commit()
		return jsonify(data = content)



@app.route("/topics/", methods=['GET'])
def get_topics():
	"""Returns 20 topics sorted by upvotes, descending"""
	topics = [topic.json() for topic in Topics.query.order_by(Topics.n_upvotes.desc()).limit(20).all()]
	return jsonify(data= topics)


@app.route("/delete-topic/", methods=['POST'])
def delete_topic():
	"""Delte a topic by ID"""
	id = request.form['id']
	if not id:
		return abort(400)
	topic = Topics.query.filter_by(id=id).first()
	db.session.delete(topic)
	db.session.commit()
	return "success"


@app.route("/upvote/<int:topic_id>/", methods=['POST'])
def upvote(topic_id):
	"""Upvote function increments the upvote count of a topic"""
	topic = Topics.query.filter_by(id=topic_id).first()
	if not topic:
		return abort(400)
	topic.n_upvotes = topic.n_upvotes + 1
	db.session.commit()
	return jsonify(data=topic.json())

@app.route("/downvote/<int:topic_id>/", methods=['POST'])
def downvote(topic_id):
	"""Downvote function increments the downvote count of a topic"""
	topic = Topics.query.filter_by(id=topic_id).first()
	if not topic:
		return abort(400)
	topic.n_downvotes = topic.n_downvotes + 1
	db.session.commit()
	return jsonify(data=topic.json())


if __name__ == '__main__':
    app.run()
