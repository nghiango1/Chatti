from ulti.Singeleton import Singleton
from user import User
from time import time
from ulti.TimeToString import timeToString


class Room():
    def __init__(self, id):
        self.message = []
        self.id = id
        self.users = []

    def getMessage(self):
        return self.message

    def join(self, user: User):
        if user in self.users:
            return
        self.users.append(user)

    def getUsers(self):
        return self.users

    def recv(self, user: User, message):
        self.message.append((time(), user, message))

    def toDict(self):
        s = {}
        s['id'] = self.id
        s['message'] = [[t, u.username, m] for t, u, m in self.message]
        return s

    def __str__(self):
        s = f"Room {self.id}:\n"
        for t, u, m in self.message:
            s += f"({timeToString(t)}) {u.username}: {m}\n"
        return s


class RoomBase(metaclass=Singleton):
    def __init__(self):
        self.rooms = {0: Room(0)}
        self.currId = 0

    def createRoom(self):
        self.currId += 1
        self.rooms.append(Room(self.currId))
        return self.currId

    def getRoom(self, id):
        if id not in self.rooms:
            return None
        return self.rooms[id]

    def getRoomList(self):
        return self.rooms.keys()

    def delRoom(self, id):
        if id in self.rooms:
            self.rooms.pop(id)


if __name__ == "__main__":
    from user import UserBase
    rb = RoomBase()
    ub = UserBase()
    r = rb.getRoom(0)
    assert r is not None
    users = ub.getUserBase()
    assert users is not None
    r.recv(users["user01"], "Hello")
    r.recv(users["user02"], "World!")
    r.recv(users["admin"], "Admin here")
    assert r.message.__len__() == 3
    print("test Room ok")
