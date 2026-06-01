
from flask import Flask, request, redirect, session, render_template_string

app = Flask(__name__)
app.secret_key = "secret123"

ROOM_CODE = "PLC2026"

LOGIN_PAGE = """
<h2>Private Chat Room</h2>
<form method="post">
<input name="username" placeholder="Your Name" required><br><br>
<input name="code" placeholder="Room Code" required><br><br>
<button type="submit">Enter</button>
</form>
"""

CHAT_PAGE = """
<h2>Private Chat Room</h2>

<div id="chat" style="height:300px;border:1px solid #000;overflow:auto;padding:10px;"></div>

<input id="msg" placeholder="Message">
<button onclick="sendMsg()">Send</button>

<script>
function sendMsg(){
 let msg = document.getElementById("msg").value;
 let box = document.getElementById("chat");
 box.innerHTML += "<p><b>You:</b> " + msg + "</p>";
 document.getElementById("msg").value="";
}
</script>
"""

@app.route("/", methods=["GET","POST"])
def login():
    if request.method == "POST":
        if request.form["code"] == ROOM_CODE:
            session["user"] = request.form["username"]
            return redirect("/chat")
        return "
