from src.ulti.Singeleton import Singleton
from typing import Dict, Optional


class User:
    def __init__(self, username, password, isAdmin=False):
        self.roles = []
        if isAdmin:
            self.roles.append("admin")
        self.username = username
        self.password = password

    def __str__(self):
        return f"User name {self.username}\n"


class UserBase(metaclass=Singleton):
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.addUser("admin", isAdmin=True)
        self.addUser("user01")
        self.addUser("user02")

    def getUser(self, name: str) -> Optional[User]:
        return self.users.get(name, None)

    def getUserList(self):
        return self.users.keys()

    def getUserBase(self):
        return self.users

    def addUser(self, name, password="1", isAdmin=False):
        if self.users.__contains__(name):
            return
        self.users[name] = User(name, password, isAdmin=isAdmin)

    def __str__(self):
        ub = ""
        for u in self.users:
            ub += u.__str__()
        return ub


if __name__ == "__main__":
    ub = UserBase()
    assert len(ub.getUserBase()) == 3
    ub.addUser("user03", "user03")
    assert len(ub.getUserBase()) == 4
    ub2 = UserBase()
    ub2.addUser("user04")
    assert len(ub.getUserBase()) == 5
    print("test User ok")
