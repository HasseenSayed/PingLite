class User:
    def __init__(self, user_id, username, first_name, last_name, email=None):
        self.user_id = user_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(
            user_id=data.get('user_id'),
            username=data.get('username'),
            first_name=data.get('user_first_name'),
            last_name=data.get('user_last_name'),
            email=data.get('user_email')
        ) 