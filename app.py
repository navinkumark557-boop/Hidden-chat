from flask import Flask, request, redirect, session, render_template_string

app = Flask(__name__)
app.secret_key = "secret123"

ROOM_CODE = "PLC2026"
messages = []

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

<div style="height:300px;border:1px solid black;overflow:auto;padding:10px;">
{% for msg in messages %}
<p><b>{{msg}}</b></p>
{% endfor %}
</div>

<form method="post">
<input name="message" placeholder="Message" required>
<button type="submit">Send</button>
</form>

<br>
<a href="/refresh">Refresh Messages</a>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["code"] == ROOM_CODE:
            session["user"] = request.form["username"]
            return redirect("/chat")
        return "Wrong Room Code"

    return render_template_string(LOGIN_PAGE)

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        msg = request.form["message"]
        messages.append(f"{session['user']}: {msg}")

    return render_template_string(CHAT_PAGE, messages=messages)

@app.route("/refresh")
def refresh():
    return redirect("/chat")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
