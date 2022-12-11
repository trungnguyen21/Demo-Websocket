from flask import Flask, request, render_template, session, redirect
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_session import Session

app = Flask(__name__)

app.debug = True
app.config['SECRET_KEY'] = 'secret'
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

socketio = SocketIO(app)

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "GET":
        return render_template("index.html") #Login

@app.route("/chat", methods=["POST", "GET"])
def chat():
    if request.method == "POST":
        user = request.form.get("username")
        session['username'] = user
        return render_template("chat.html", session = session)
    if request.method == "GET":
        return redirect("/")

@socketio.on('join', namespace='/chat')
def join(message):
    room = "Chatroom"
    join_room(room)
    emit('status', {'msg':  session.get('username') + ' has entered the room.'}, room=room)


@socketio.on('text', namespace='/chat')
def text(message):
    room = "Chatroom"
    emit('message', {'msg': session.get('username') + ' : ' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    room = "Chatroom"
    username = session.get('username')
    leave_room(room)
    session.clear()
    emit('status', {'msg': username + ' has left the room.'}, room=room)


if __name__ == '__main__':
    socketio.run(app)