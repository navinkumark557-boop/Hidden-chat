from flask import Flask, request, session, redirect, render_template_string
from flask_socketio import SocketIO, emit
import time
import threading

app = Flask(__name__)
app.secret_key = "secret123"

socketio = SocketIO(app, cors_allowed_origins="*")

ROOM_CODE = "Nnnnnnnn"
messages = []

LOGIN_HTML = """
<!DOCTYPE html>
<html>
<body>
<h2>Private Chat Login</h2>

<form method="post">
<input name="username" placeholder="Your Name" required><br><br>
<input name="code" placeholder="Room Code" required><br><br>
<button type="submit">Enter Chat</button>
</form>

</body>
</html>
"""

CHAT_HTML = """
<!DOCTYPE html>
<html>
<head>
<title>Live Chat</title>

<script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.7.2/socket.io.js"></script>

<script>
var socket = io();

socket.on("new_message", function(data){
    loadMessages(data.messages);
});

function sendMessage(){
    let msg = document.getElementById("msg").value;

    socket.emit("send_message", {
        message: msg,
        user: "{{user}}"
    });

    document.getElementById("msg").value="";
}

function loadMessages(msgs){
    let box = document.getElementById("chat");
    box.innerHTML="";

    msgs.forEach(function(m){
        box.innerHTML += "<p><b>" + m.user + ":</b> " + m.text + "</p>";
    });

    box.scrollTop = box.scrollHeight;
}
</script>

</head>
<body>

<h2>Private Chat Room</h2>

<div id="chat"
style="height:350px;border:1px solid black;overflow:auto;padding:10px;">
</div>

<input id="msg" placeholder="Message">
<button onclick="sendMessage()">Send</button>

</body>
</html>
"""
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["code"] == ROOM_CODE:
            session["user"] = request.form["username"]
            return redirect("/chat")
        return "Wrong Room Code"

    return LOGIN_HTML


@app.route("/chat")
def chat():
    if "user" not in session:
        return redirect("/")

    return render_template_string(
        CHAT_HTML,
        user=session["user"]
    )


@socketio.on("connect")
def connect():
    emit("new_message", {"messages": messages})


@socketio.on("send_message")
def send_message(data):
    global messages

    messages.append({
        "user": data["user"],
        "text": data["message"],
        "time": time.time()
    })

    emit(
        "new_message",
        {"messages": messages},
        broadcast=True
    )


def cleanup_messages():
    global messages

    while True:
        now = time.time()

        messages = [
            m for m in messages
            if now - m["time"] < 30
        ]

        socketio.emit(
            "new_message",
            {"messages": messages}
        )

        time.sleep(2)


threading.Thread(
    target=cleanup_messages,
    daemon=True
).start()


if __name__ == "__main__":
    socketio.run(
        app,
        host="0.0.0.0",
        port=5000
    )
