from flask import Flask, request, redirect, session, render_template_string
import time

app = Flask(__name__)
app.secret_key = "secret123"

ROOM_CODE = "PLC2026"
messages = []

LOGIN_HTML = """
<h2>Private Chat Room</h2>
<form method="post">
<input name="username" placeholder="Your Name" required><br><br>
<input name="code" placeholder="Room Code" required><br><br>
<button type="submit">Enter</button>
</form>
"""

CHAT_HTML = """
<!DOCTYPE html>
<html>
<head>
<meta http-equiv="refresh" content="60">
<title>Private Chat</title>
</head>
<body>

<h2>Private Chat Room</h2>

<div style="height:300px;border:1px solid black;overflow:auto;padding:10px;">
{% for msg in messages %}
<p>{{ msg }}</p>
{% endfor %}
</div>

<form method="post">
<input name="message" placeholder="Message" required>
<button type="submit">Send</button>
</form>

<form action="/clear" method="post">
<button type="submit">Clear Chat</button>
</form>

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

    return render_template_string(LOGIN_HTML)

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user" not in session:
        return redirect("/")

    now = time.time()

    global messages
    messages = [m for m in messages if now - m["time"] < 30]

    if request.method == "POST":
        text = request.form["message"]
        messages.append({
            "user": session["user"],
            "text": text,
            "time": now
        })

    display = [f"{m['user']}: {m['text']}" for m in messages]

    return render_template_string(CHAT_HTML, messages=display)

@app.route("/clear", methods=["POST"])
def clear():
    global messages
    messages = []
    return redirect("/chat")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
