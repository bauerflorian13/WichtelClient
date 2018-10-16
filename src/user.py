class User(object):
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.forbidden = []

    def forbid(self, other):
        self.forbidden.append(other)

    def is_forbidden(self, other):
        return other in self.forbidden