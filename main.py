import functools
from flask import (Flask, jsonify, request, abort,
                   render_template, g, Blueprint, flash,
                   redirect, session, url_for)

from flask_socketio import SocketIO, send, emit
from src.room import RoomBase, Message
from src.user import UserBase


app = Flask(__name__)


@app.after_request
def add_cache_control(response):
    if request.path.endswith('/static/tailwind.css'):
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
    return response


def admin_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        if not g.isAdmin:
            abort(401)

        return view(**kwargs)

    return wrapped_view


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view


@app.route('/api/user', methods=['GET'])
@admin_required
def get_user():
    ub = UserBase()
    return jsonify(list(ub.getUserList()))


@app.route('/api/createroom', methods=['GET'])
@admin_required
def create_room():
    rb = RoomBase()
    id = rb.createRoom()
    return jsonify({"message": "success",'room_id': id})


@app.route('/api/iam', methods=['GET'])
def whoami():
    return jsonify({'user': session['user_id'], 'roles': g.roles, 'isAdmin': g.isAdmin})


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
    if username is None:
        abort(401)
    u = ub.getUser(username)
    if u is None:
        abort(401)
    message = Message(username, request.args.get("message"))
    r.recv(message)
    return jsonify({"message": "Room recv message"})


def getRoomAndUrlList():
    rb = RoomBase()
    roomWithUrl = [(rid, f"/room/{rid}") for rid in rb.getRoomList()]
    return roomWithUrl


@app.route('/')
def index():
    rb = RoomBase()
    r = rb.getRoom(0)
    session['room_id'] = 0
    message = r.getMessage()
    return render_template('index.html', message=message, room=getRoomAndUrlList(), curr = 0)


@app.route('/room/<int:room_id>')
def room(room_id: int):
    rb = RoomBase()
    r = rb.getRoom(room_id)
    if r is None:
        abort(404)
    session['room_id'] = room_id
    message = r.getMessage()
    return render_template('index.html', message=message, room=getRoomAndUrlList(), curr = room_id)


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            ub = UserBase()
            if ub.getUser(username) is not None:
                error = f"User {username} is already registered."
            else:
                ub.addUser(username, password)
                return redirect(url_for("auth.login"))
        else:
            flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None

        ub = UserBase()
        u = ub.getUser(username)

        if u is None:
            error = 'Incorrect username.'
        elif u.password != password:
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = u.username
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        ub = UserBase()
        u = ub.getUser(user_id)
        g.user = u
        g.isAdmin = False
        if u.roles:
            g.roles = u.roles
            g.isAdmin = u.roles.__contains__("admin")


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


connected_users = set()
soc = SocketIO(app)


def soc_login_required(view):
    @functools.wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            emit('alert', {'message': 'You are not authorized.',
                 'url': url_for('auth.login')})
            return redirect(url_for('auth.login'))
        return view(*args, **kwargs)
    return wrapped_view


@soc.on('message')
@soc_login_required
def handle_message(message):
    rb = RoomBase()
    r = rb.getRoom(session['room_id'])
    if r is None:
        abort(404)
    m = Message(session['user_id'], message)
    r.recv(m)
    send(m.toHtml(), broadcast=True)


@soc.on('join')
def handle_join(data):
    username = data['username']
    connected_users.add(username)
    send(username + ' has joined the chat.', broadcast=True)


@soc.on('leave')
def handle_leave(data):
    username = data['username']
    connected_users.remove(username)
    send(username + ' has left the chat.', broadcast=True)


app.register_blueprint(bp)
app.config.from_mapping(
    SECRET_KEY='dev',
)


def main():
    soc.run(app, host='0.0.0.0', debug=True)


if __name__ == "__main__":
    main()
