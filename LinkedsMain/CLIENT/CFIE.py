import re


class User:

    def __init__(self, login, password=None, email=None, name=None, status=None):
        self.methods = {}
        for key, value in User.__dict__.items():
            if key[:2] != '__' and key[-2:] != '__':
                self.methods[f"<{key.upper().replace('_', '-')}>"] = key

        self.login = login
        if password is not None:
            self.password = password
        if email is not None:
            self.email = email
        if name is not None:
            self.name = name
        if status is not None:
            self.status = status

    def __str__(self) -> str:
        return f"Login:{self.login}|Password:{self.password}|Email:{self.email}"

    def __getattr__(self, item) -> str:
        return f"Attribute '{item}' does not exist."

    def __setattr__(self, key, value) -> None:
        if key == 'methods':
            self.__dict__[key] = value
            return
        status = self.call_method(f"<{key.upper()}>")(value)
        if status != '<SUCCESS>':
            raise ValueError(status)
        self.__dict__[key] = value

    def call_method(self, method: str = None):
        """
        Return object of class method

        <- str[<EMAIL>]
        if exist
            -> class method["method"]
        else
            raise error
        """
        method_call = self.methods.get(method)
        if method_call is None:
            return False
        return getattr(self, method_call)

    @classmethod
    def name(cls, data: str = None) -> str:
        if not cls.check_data(data):
            return 'Вместо пробелов используйте знак "_"!'
        if not cls.alphabet(data, 'name'):
            return 'Использованы запрещенные знаки!\nРазрешенные: "а-я", "А-Я", "a-z", "A-Z"'
        if len(data) < 6:
            return 'Имя должно быть хотя бы из 6 символов!'
        if len(data) > 40:
            return 'Имя не должно превышать 40 символов!'
        return '<SUCCESS>'

    @classmethod
    def status(cls, data: str = None) -> str:
        if not cls.check_data(data):
            return 'Вместо пробелов используйте знак "_"!'
        if not cls.alphabet(data, 'status'):
            return 'Использованы запрещенные знаки!\nРазрешенные: "а-я", "А-Я", "a-z", "A-Z", "0-9", "_!@#$%&()"'
        if len(data) < 1:
            return 'Статус должен быть хотя бы из 1 символа!'
        if len(data) > 80:
            return 'Статус не должен превышать 80 символов!'
        return '<SUCCESS>'

    @classmethod
    def email(cls, data: str = None) -> str:
        if type(data) is not str:
            return '<DENIED>'
        if not cls.check_data(data):
            return 'Вместо пробелов используйте знак "_"!'
        pattern = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})"
        match = re.fullmatch(pattern, data)
        if match is not None:
            return '<SUCCESS>'
        else:
            return 'Такой Эл.Почты не существует'

    @classmethod
    def login(cls, data: str = None) -> str:
        if not cls.check_data(data):
            return 'Вместо пробелов используйте знак "_"!'
        if not cls.alphabet(data):
            return 'Использованы запрещенные знаки!\nРазрешенные: "a-z", "A-Z", "0-9", "_!@#$%&()"'
        cnt = 0
        for el in data:
            if el.lower() in [i for i in 'qwertyuiopasdfghjklzxcvbnm']:
                cnt += 1
        if cnt == 0:
            return 'В логине должна быть хотя бы одна буква латинского алфавита!'
        if len(data) < 3:
            return 'Логин должен быть хотя бы из 3 символов!'
        if len(data) > 25:
            return 'Логин не должен превышать 25 символов!'
        return '<SUCCESS>'

    @classmethod
    def password(cls, data: str = None) -> str:
        if not cls.check_data(data):
            return 'Вместо пробелов используйте знак "_"!'
        if not cls.alphabet(data):
            return 'Использованы запрещенные знаки!\nРазрешенные: "a-z", "A-Z", "0-9", "_!@#$%&()"'
        cnt = 0
        for el in data:
            if el.lower() in [i for i in 'qwertyuiopasdfghjklzxcvbnm']:
                cnt += 1
        if cnt == 0:
            return 'В пароле должна быть хотя бы одна буква латинского алфавита!'
        if len(data) < 6:
            return 'Пароль должен быть хотя бы из 6 символов!'
        if len(data) > 60:
            return 'Пароль не должен превышать 60 символов!'
        return '<SUCCESS>'

    @classmethod
    def check_data(cls, data: str = None) -> bool:
        if data.isspace():
            return False
        if data == '':
            return False
        return True

    @classmethod
    def alphabet(cls, data: str = None, status: str = 'None') -> bool:
        """
        If the string consists of [A-Z][a-z][0-9] return True
        else return False

        data: str
        return -> bool
        """
        if type(data) is not str:
            return False
        if status == 'name':
            pattern = r"[а-яА-Яa-zA-ZёЁ ]+"
        elif status == 'status':
            pattern = r"[а-яА-Яa-zA-Z0-9_!@#$%&()ёЁ?,:; ]+"
        else:
            pattern = r"[a-zA-Z0-9_!@#$%&()]+"
        match = re.fullmatch(pattern, data)
        if match is None:
            return False
        return True


if __name__ == '__main__':
    ...
