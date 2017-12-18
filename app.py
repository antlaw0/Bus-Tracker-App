from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)

socketio = SocketIO(app)


@app.route('/')
def home_page():
    return render_template("index.html")


@socketio.on('new_message')
def handle_new_message(message):
    print("New message recieved: ", message)
    # Broadcast the messsage to all connected clients.
    emit("new_message_received", message, broadcast=True)



if __name__ == '__main__':
    socketio.run(app, host="https://agile-sea-57808.herokuapp.com")