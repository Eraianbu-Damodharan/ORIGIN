from flask import Flask, request, render_template_string

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Demo Vulnerable App</title>
</head>
<body>
    <h1>Demo Vulnerable App</h1>

    <h2>Search</h2>
    <form method="GET" action="/search">
        <input type="text" name="q" placeholder="Search term">
        <button type="submit">Search</button>
    </form>

    <h2>Login</h2>
    <form method="POST" action="/login">
        <input type="text" name="username" placeholder="Username">
        <input type="text" name="password" placeholder="Password">
        <button type="submit">Login</button>
    </form>

    <h2>Comment</h2>
    <form method="POST" action="/comment">
        <input type="text" name="comment" placeholder="Write comment">
        <button type="submit">Submit</button>
    </form>
</body>
</html>
"""

@app.route("/")
def home():
    return HTML


@app.route("/search")
def search():
    q = request.args.get("q", "")
    return f"<h2>Search Results for: {q}</h2>"


@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if "'" in username or '"' in username:
        return "SQL syntax error near input", 500

    return f"Welcome {username}"


@app.route("/comment", methods=["POST"])
def comment():
    comment = request.form.get("comment", "")
    return render_template_string(f"<h3>User Comment:</h3><div>{comment}</div>")


if __name__ == "__main__":
    app.run(debug=True)