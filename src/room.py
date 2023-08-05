from typing import List, Dict
from src.ulti.Singeleton import Singleton
from src.user import UserBase, User
from time import time
from src.ulti.TimeToString import timeToString


class Message():
    def __init__(self, username, message):
        self.username = username
        self.message = message
        self.time = time()

    def getUser(self):
        ub = UserBase()
        u = ub.getUser(self.username)
        return u

    def getTime(self):
        return timeToString(self.time)

    def __str__(self):
        return f"({timeToString(self.time)}) {self.username}: {self.message}\n"

    def toHtml(self):
        return f"<p>({timeToString(self.time)}) <strong>{self.username}</strong>: {self.message}</p>"

    def toList(self):
        return [self.time, self.username, self.message]


class Room():
    def __init__(self, id: int, users: User = [], message: List[Message] = []):
        self.message: List[Message] = []
        self.id = id
        self.users = []

    def getMessage(self):
        return self.message

    def join(self, username: str):
        if self.users.__contains__(username):
            return
        self.users.append(username)

    def getUsers(self):
        return self.users

    def recv(self, message: Message):
        self.message.append(message)

    def toDict(self):
        s = {}
        s['id'] = self.id
        s['message'] = [m.toList() for m in self.message]
        return s

    def __str__(self):
        s = f"Room {self.id}:\n"
        for mo in self.message:
            t, u, m = mo.toList()
            s += f"({timeToString(t)}) {u}: {m}\n"
        return s


class RoomBase(metaclass=Singleton):
    def __init__(self):
        self.rooms: Dict[int, Room] = {0: Room(0)}
        self.currId = 0

    def createRoom(self):
        self.currId += 1
        self.rooms[self.currId] = Room(self.currId)
        return self.currId

    def getRoom(self, id) -> Room:
        if id not in self.rooms:
            return None
        return self.rooms[id]

    def getRoomList(self) -> List[int]:
        return self.rooms.keys()

    def delRoom(self, id):
        if id in self.rooms:
            self.rooms.pop(id)


if __name__ == "__main__":
    rb = RoomBase()
    r = rb.getRoom(0)
    assert r is not None
    r.recv(Message("user01", "Hello"))
    r.recv(Message("user02", "world"))
    r.recv(Message("user01", "Hello"))
    assert r.message.__len__() == 3
    print("test Room ok")
