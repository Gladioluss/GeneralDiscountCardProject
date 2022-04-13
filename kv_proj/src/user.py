class User:
    object_name: str = 'User'
    login: str
    password: str

    def __init__(self, login, password):
        self.login = login
        self.password = password

