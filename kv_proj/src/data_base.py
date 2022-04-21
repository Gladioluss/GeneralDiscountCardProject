import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
from kv_proj.src.user import User

import kv_proj.src.hash_password

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

    def add_new_user(self, login, password) -> None:
        user = User(login, password)
        ref = db.reference('/')
        ref.child('users').update({
                f'user_{user.login}': {
                    'login': user.login,
                    'password': user.password,
                    'card_list': {
                        '0': '-1'
                    }
                    }
                })

    def check_user_exists(self, login) -> object:
        ref = db.reference('/')
        res = ref.child('users').child(f'user_{login}').get()
        return res

    def add_new_card(self, login, card_name) -> None:
        ref = db.reference('/')
        card_list = ref.child('users').child(f'user_{login}').child('card_list').get()
        new_card_number = len(card_list)
        if new_card_number == 1:
            ref.child('users').child(f'user_{login}').child('card_list').child('0').delete()
        ref.child('users').child(f'user_{login}').child('card_list').update({card_name: card_name})

    def delete_card(self, login, card_number) -> None:
        ref = db.reference('/')
        ref.child('users').child(f'user_{login}').child('card_list').child(card_number).delete()




