class User(object):
    def __init__(self, name):
        self.name = name
        self.forbidden = []

    def getName(self):
        return self.name

    def forbid(self, other):
        self.forbidden.append(other)

    def isForbidden(self, other):
        return other in self.forbidden