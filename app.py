from flask import Flask, render_template, request, jsonify, abort
from models import db, Topics
from flask_heroku import Heroku

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/reddit'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
heroku = Heroku(app)
db.init_app(app)

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


@app.route("/up-vote/", methods=['POST'])
def upvote():
	"""Upvote function increments the upvote count of a topic"""
	topic_id = request.args.get("id")
	topic = Topics.query.filter_by(id=topic_id).first()
	if not topic:
		return abort(400)
	topic.n_upvotes = topic.n_upvotes + 1
	db.session.commit()
	return jsonify(topic.json())

@app.route("/down-vote/", methods=['POST'])
def downvote():
	"""Downvote function increments the downvote count of a topic"""
	topic_id = request.args.get("id")
	topic = Topics.query.filter_by(id=topic_id).first()
	if not topic:
		return abort(400)
	topic.n_downvotes = topic.n_downvotes + 1
	db.session.commit()
	return jsonify(topic.json())


if __name__ == '__main__':
    app.run()
