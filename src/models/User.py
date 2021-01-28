import uuid

from flask import session

from src.common.database import Database


class User(object):
    def __init__(self, name, email, password, _id=None):
        self.name = name
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("users", {'email': email})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_validate(email, password):
        user = User.get_by_email(email)
        if user is not None and user.password == password:
            return user.name

    @classmethod
    def register(cls, name, email, password):
        user = cls.get_by_email(email)
        if user is None:
            new_user = cls(name, email, password)
            new_user.save_to_mongo()
            return True
        else:
            return False

    @staticmethod
    def login(user_email):
        session['email'] = user_email
        session['type'] = 'user'

    @staticmethod
    def logout():
        session['email'] = None
        session['name'] = None

    def json(self):
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "_id": self._id
        }

    def save_to_mongo(self):
        Database.insert("users", self.json())
