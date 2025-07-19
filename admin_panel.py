import os
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)
DATABASE_FILE = "database.json"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")

def load_data():
    if not os.path.exists(DATABASE_FILE):
        return {}
    with open(DATABASE_FILE, "r") as f:
        return json.load(f)

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        password = request.form.get("password")
        if password == ADMIN_PASSWORD:
            return redirect(url_for("admin"))
        else:
            return "Incorrect password", 403
    return '''
    <form method="post">
      Admin Password: <input type="password" name="password"/>
      <input type="submit" value="Login"/>
    </form>
    '''

@app.route("/admin")
def admin():
    data = load_data()
    return render_template("index.html", users=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
