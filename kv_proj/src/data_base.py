import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from kv_proj.src.user import User
from os import getenv
from dotenv import load_dotenv
import json


load_dotenv()
FIREBASE_API_KEY = {
        "type": getenv("TYPE"),
        "project_id": getenv("PROJECT_ID"),
        "private_key_id": getenv("PRIVATE_KEY_ID"),
        "private_key": getenv("PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": getenv("CLIENT_EMAIL"),
        "client_id": getenv("CLIENT_ID"),
        "auth_uri": getenv("AUTH_URI"),
        "token_uri": getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url": getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": getenv("CLIENT_X509_CERT_URL")

}
URL_DATABASE = getenv("URL_DATABASE")


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
            cred = credentials.Certificate(FIREBASE_API_KEY)
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




