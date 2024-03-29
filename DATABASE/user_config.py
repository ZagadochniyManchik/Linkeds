import pickle


class StandardMethods:

    def set_items(self, items):
        if len(self.__dict__.items()) != len(items.items()):
            raise ValueError('Items length doesnt match to self.__dict__')
        self.__dict__ = items

    def set_exist_items(self, data):
        for key, value in data.items():
            self.__dict__[key] = value


class User(StandardMethods):

    def __init__(self):
        self.id = None
        self.ip = None
        self.online = 'False'
        self.login = None
        self.password = None
        self.email = 'Не указано'
        self.gender = 'Не указано'
        self.name = 'Не указано'
        self.status = 'Не указано'
        self.deleted_status = 'False'


class Social(StandardMethods):

    def __init__(self):
        self.id = None
        self.pfp = None
        self.posts = None
        self.friends = None
        self.messages = None
        self.request_friends = None
        self.black_list_friends = None


class Connection(StandardMethods):

    def __init__(self):
        self.ip = None
        self.id = None
        self.user_data = None


class Message(StandardMethods):

    def __init__(self):
        self.from_ = None
        self.to_ = None
        self.id = None
        self.status = None
        self.text = None
        self.time = None
        self.image = None


if __name__ == '__main__':
    ...
