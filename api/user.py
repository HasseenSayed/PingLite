import json

class User():
    def __init__(self, username, first_name, last_name, password,):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)