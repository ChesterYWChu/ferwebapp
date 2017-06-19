from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import datetime
# from sqlalchemy import desc
import logging

builtin_list = list

db = SQLAlchemy()

def init_app(app):
    # Disable track modifications, as it unnecessarily uses memory.
    app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
    db.init_app(app)

def from_sql(row):
    """Translates a SQLAlchemy model instance into a dictionary"""
    data = row.__dict__.copy()
    data['id'] = row.id
    data.pop('_sa_instance_state')
    return data

# [START model]
class Result(db.Model):
    __tablename__ = 'result'

    id = db.Column(db.Integer, primary_key=True)
    predictions = db.Column(db.String(4096))
    image_url = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __repr__(self):
        return "<Result(id=%d, image_url='%s', predictions='%s')" % (self.id, self.image_url, self.predictions)
# [END model]

# [START list]
def list(limit=10, cursor=None):
    cursor = int(cursor) if cursor else 0
    query = (Result.query
             .order_by(db.desc(Result.created_date))
             .limit(limit)
             .offset(cursor))
    logger = logging.getLogger('')
    logger.info('2==========')
    logger.info(db.engine.url)
    results = builtin_list(map(from_sql, query.all()))
    next_page = cursor + limit if len(results) == limit else None
    return (results, next_page)
# [END list]

# [START create]
def create(data):
    result = Result(**data)
    db.session.add(result)
    db.session.commit()
    return from_sql(result)
# [END create]

def _create_database():
    """
    If this script is run directly, create all the tables necessary to run the
    application.
    """
    app = Flask(__name__)
    # app.config.from_object(config)
    app.config.from_pyfile('../config.py')
    init_app(app)
    with app.app_context():
        db.create_all()
    print("All tables created")


if __name__ == '__main__':
    _create_database()