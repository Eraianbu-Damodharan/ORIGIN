from flask import Flask, request

app = Flask(__name__)

BASE_STYLE = """
<style>
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    body {
        background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
        color: white;
        min-height: 100vh;
        padding: 40px;
    }

    .container {
        max-width: 1100px;
        margin: auto;
    }

    .hero {
        text-align: center;
        margin-bottom: 40px;
    }

    .hero h1 {
        font-size: 3rem;
        color: #38bdf8;
        margin-bottom: 10px;
        text-shadow: 0 0 18px rgba(56, 189, 248, 0.35);
    }

    .hero p {
        color: #cbd5e1;
        font-size: 1.1rem;
    }

    .grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 24px;
        margin-top: 30px;
    }

    .card {
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 24px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        transition: transform 0.25s ease, box-shadow 0.25s ease;
    }

    .card:hover {
        transform: translateY(-6px);
        box-shadow: 0 18px 40px rgba(0,0,0,0.4);
    }

    .badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-bottom: 14px;
    }

    .badge.xss {
        background: rgba(239, 68, 68, 0.2);
        color: #fca5a5;
        border: 1px solid rgba(239, 68, 68, 0.35);
    }

    .badge.sqli {
        background: rgba(34, 197, 94, 0.18);
        color: #86efac;
        border: 1px solid rgba(34, 197, 94, 0.35);
    }

    .badge.comment {
        background: rgba(168, 85, 247, 0.18);
        color: #d8b4fe;
        border: 1px solid rgba(168, 85, 247, 0.35);
    }

    .card h2 {
        margin-bottom: 10px;
        font-size: 1.4rem;
    }

    .card p {
        color: #cbd5e1;
        line-height: 1.6;
        margin-bottom: 18px;
    }

    .btn {
        display: inline-block;
        text-decoration: none;
        background: linear-gradient(90deg, #06b6d4, #3b82f6);
        color: white;
        padding: 10px 18px;
        border-radius: 12px;
        font-weight: 600;
        transition: opacity 0.2s ease;
    }

    .btn:hover {
        opacity: 0.9;
    }

    .panel {
        max-width: 700px;
        margin: 50px auto 0;
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.12);
        backdrop-filter: blur(12px);
        border-radius: 20px;
        padding: 28px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }

    .panel h2 {
        margin-bottom: 12px;
        color: #38bdf8;
    }

    .panel p {
        margin-bottom: 18px;
        color: #cbd5e1;
    }

    input, textarea {
        width: 100%;
        padding: 14px 16px;
        margin-bottom: 16px;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.15);
        background: rgba(255,255,255,0.08);
        color: white;
        outline: none;
    }

    input::placeholder, textarea::placeholder {
        color: #94a3b8;
    }

    button {
        background: linear-gradient(90deg, #06b6d4, #2563eb);
        color: white;
        padding: 12px 20px;
        border: none;
        border-radius: 12px;
        cursor: pointer;
        font-weight: 600;
    }

    button:hover {
        opacity: 0.92;
    }

    .result {
        margin-top: 20px;
        padding: 16px;
        border-radius: 14px;
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(255,255,255,0.1);
    }

    .nav {
        margin-bottom: 24px;
    }

    .nav a {
        color: #7dd3fc;
        text-decoration: none;
        margin-right: 18px;
        font-weight: 600;
    }

    .footer {
        text-align: center;
        margin-top: 40px;
        color: #94a3b8;
        font-size: 0.95rem;
    }
</style>
"""


@app.route("/")
def home():
    return f"""
    <html>
    <head>
        <title>Aegis Hybrid Demo Lab</title>
        {BASE_STYLE}
    </head>
    <body>
        <div class="container">
            <div class="hero">
                <h1>Aegis Hybrid Demo Lab</h1>
                <p>Interactive vulnerable web application for adaptive security intelligence testing</p>
            </div>

            <div class="grid">
                <div class="card">
                    <div class="badge xss">Reflected XSS</div>
                    <h2>Search Module</h2>
                    <p>Test reflected input handling and observe how injected scripts appear in the response.</p>
                    <a class="btn" href="/search">Open Search Lab</a>
                </div>

                <div class="card">
                    <div class="badge sqli">SQL Injection</div>
                    <h2>Login Module</h2>
                    <p>Test input-based authentication vulnerabilities and trigger simulated backend SQL errors.</p>
                    <a class="btn" href="/login">Open Login Lab</a>
                </div>

                <div class="card">
                    <div class="badge comment">Input Reflection</div>
                    <h2>Comment Module</h2>
                    <p>Submit comments and analyze how reflected content changes the server response behavior.</p>
                    <a class="btn" href="/comment">Open Comment Lab</a>
                </div>
            </div>

            <div class="footer">
                Built for security scanning demonstration and judge-facing presentation
            </div>
        </div>
    </body>
    </html>
    """


@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q", "")
    return f"""
    <html>
    <head>
        <title>Search Lab</title>
        {BASE_STYLE}
    </head>
    <body>
        <div class="container">
            <div class="nav">
                <a href="/">Home</a>
                <a href="/login">Login Lab</a>
                <a href="/comment">Comment Lab</a>
            </div>

            <div class="panel">
                <h2>Search Module - Reflected XSS Test</h2>
                <p>Try entering a normal search term or a test payload like <b>&lt;script&gt;alert(1)&lt;/script&gt;</b>.</p>

                <form method="GET" action="/search">
                    <input type="text" name="q" placeholder="Search here..." value="{q}">
                    <button type="submit">Search</button>
                </form>

                <div class="result">
                    <strong>Search Result:</strong><br><br>
                    Results for: {q}
                </div>
            </div>
        </div>
    </body>
    </html>
    """


@app.route("/login", methods=["GET", "POST"])
def login():
    message = ""

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        if "'" in username or '"' in username:
            return f"""
            <html>
            <head>
                <title>Login Lab</title>
                {BASE_STYLE}
            </head>
            <body>
                <div class="container">
                    <div class="nav">
                        <a href="/">Home</a>
                        <a href="/search">Search Lab</a>
                        <a href="/comment">Comment Lab</a>
                    </div>

                    <div class="panel">
                        <h2>Login Module - SQL Injection Test</h2>
                        <p>This module simulates a vulnerable backend.</p>
                        <div class="result">
                            SQL syntax error near input: mysql error: unclosed quotation mark
                        </div>
                    </div>
                </div>
            </body>
            </html>
            """, 500

        message = f"Welcome {username}"

    return f"""
    <html>
    <head>
        <title>Login Lab</title>
        {BASE_STYLE}
    </head>
    <body>
        <div class="container">
            <div class="nav">
                <a href="/">Home</a>
                <a href="/search">Search Lab</a>
                <a href="/comment">Comment Lab</a>
            </div>

            <div class="panel">
                <h2>Login Module - SQL Injection Test</h2>
                <p>Use normal credentials or test SQL-style payloads in the username field.</p>

                <form method="POST" action="/login">
                    <input type="text" name="username" placeholder="Username">
                    <input type="password" name="password" placeholder="Password">
                    <button type="submit">Login</button>
                </form>

                {"<div class='result'><strong>Status:</strong><br><br>" + message + "</div>" if message else ""}
            </div>
        </div>
    </body>
    </html>
    """


@app.route("/comment", methods=["GET", "POST"])
def comment():
    comment_text = ""

    if request.method == "POST":
        comment_text = request.form.get("comment", "")

    return f"""
    <html>
    <head>
        <title>Comment Lab</title>
        {BASE_STYLE}
    </head>
    <body>
        <div class="container">
            <div class="nav">
                <a href="/">Home</a>
                <a href="/search">Search Lab</a>
                <a href="/login">Login Lab</a>
            </div>

            <div class="panel">
                <h2>Comment Module - Reflection Test</h2>
                <p>Submit a comment and observe how the content is reflected in the output.</p>

                <form method="POST" action="/comment">
                    <textarea name="comment" rows="5" placeholder="Write your comment here...">{comment_text}</textarea>
                    <button type="submit">Post Comment</button>
                </form>

                <div class="result">
                    <strong>Latest Comment:</strong><br><br>
                    {comment_text}
                </div>
            </div>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    print("\n[INFO] Starting vulnerable demo server...")
    print("[INFO] Open in browser: http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)