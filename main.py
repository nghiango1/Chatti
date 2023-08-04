from flask import Flask, jsonify, request, abort, render_template
from room import RoomBase
from user import UserBase


app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')


@app.route('/api/user', methods=['GET'])
def get_user():
    ub = UserBase()
    return jsonify(list(ub.getUserList()))


@app.route('/api/room', methods=['GET'])
def get_room():
    rb = RoomBase()
    return jsonify(list(rb.getRoomList()))


@app.route('/api/room/<int:room_id>', methods=['GET'])
def get_room_id(room_id: int):
    rb = RoomBase()
    r = rb.getRoom(room_id)
    if r is None:
        abort(404)
    s = {}
    s['user'] = r.getUsers()
    s['data'] = r.toDict()
    return jsonify(s)


@app.route('/api/room/<int:room_id>/send', methods=['GET'])
def send_room_id(room_id: int):
    rb = RoomBase()
    r = rb.getRoom(room_id)
    if r is None:
        abort(404)
    username = request.args.get("user")
    ub = UserBase()
    u = ub.getUser(username)
    if u is None:
        abort(401)
    message = request.args.get("message")
    r.recv(u, message)
    return jsonify({"message": "Room recv message"})

# @app.route('/api/user/<int:data_id>', methods=['GET'])
# def get_data_by_id(data_id):
#     item = next((item for item in data if item['id'] == data_id), None)
#     if item:
#         return jsonify(item)
#     else:
#         return jsonify({'message': 'Data not found'}), 404
#
#
# @app.route('/')
# def hello():
#     return 'Hello, this is a simple API!'
#
#
# @app.route('/api/data', methods=['GET'])
# def get_data():
#     return jsonify(data)
#
#
# @app.route('/api/data/<int:data_id>', methods=['GET'])
# def get_data_by_id(data_id):
#     item = next((item for item in data if item['id'] == data_id), None)
#     if item:
#         return jsonify(item)
#     else:
#         return jsonify({'message': 'Data not found'}), 404


def main():
    app.run(host='0.0.0.0', debug=True)
    pass


if __name__ == "__main__":
    main()
