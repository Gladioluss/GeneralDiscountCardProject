import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


URL_DATABASE = 'https://alphabankproject-default-rtdb.asia-southeast1.firebasedatabase.app/.json'
PATH_TO_KEY = 'serviceAccountKey.json'


def main():
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


if __name__ == '__main__':
    main()
