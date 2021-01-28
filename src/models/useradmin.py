from flask import session

from src.common.database import Database


class UserAdmin(object):
    def __init__(self, email, password, name, _id):
        self.email = email
        self.password = password
        self.name = name
        self._id = _id

    @classmethod
    def get_by_email(cls, email):
        data = Database.find_one("useradmin", {'email': email})
        if data is not None:
            return cls(**data)

    @staticmethod
    def login_validate(email, password):
        user = UserAdmin.get_by_email(email)
        if user is not None and user.password == password:
            return user.name
        else:
            return None

    @staticmethod
    def login(user):
        session['name'] = user
        session['type'] = 'admin'

    @staticmethod
    def logout():
        session['name'] = None
        session['type'] = None
