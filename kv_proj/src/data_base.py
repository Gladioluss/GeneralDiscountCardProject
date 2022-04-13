import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from kv_proj.src.user import User
import hashlib

URL_DATABASE = 'https://alphabankproject-default-rtdb.asia-southeast1.firebasedatabase.app/.json'
PATH_TO_KEY = 'serviceAccountKey.json'


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=MetaSingleton):
    connection = None

    def connect(self):
        if self.connection is None:
            cred = credentials.Certificate(PATH_TO_KEY)
            firebase_admin.initialize_app(cred, {
                'databaseURL': URL_DATABASE
            })

            self.connection = 1
            return Database

    def add_new_user(self, login, password):
        user = User(login, password)
        ref = db.reference('/')
        users_ref = ref.child('users')
        hash = hashlib.sha256()
        users_ref.update({
                f'user_{user.login}': {
                    'login': user.login,
                    'password': user.password,
                    }
                })

    def check_user_exists(self, login):
        ref = db.reference('/')
        res = ref.child('users').child(f'user_{login}').get()
        return res


# realtime database
"""
cred = credentials.Certificate(PATH_TO_KEY)
firebase_admin.initialize_app(cred, {
        'databaseURL': URL_DATABASE
    })

    ref = db.reference('/')
    ref.set({
        'Employee':
            {
                'emp1': {
                    'name': 'Danil',
                    'lname': 'Emurashin',
                    'age': 24
                }
            }
    })
"""

# firestore database
"""
def main():
    cred = credentials.Certificate(PATH_TO_KEY)
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    db.collection('people').add({'name': 'Danil', 'lname': 'Emurashin', 'age': 24})
"""
