from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }


class UserInfo(BaseModel, db.Model):
    """Model for the stations table"""
    __tablename__ = 'User Information'

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String)
    mobile = db.Column(db.String)

    def __init__(self, name, mobile):
        self.name = name
        self.mobile = mobile

    def __repr__(self):
        return '<id {}>'.format(self.id)
