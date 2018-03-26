from flask_sqlalchemy import SQLAlchemy
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