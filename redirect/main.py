import os

from dotenv import load_dotenv
from flask import Flask, redirect, request

load_dotenv()

app = Flask(__name__)

APP_URL = os.environ["APP_URL"]
methods = ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS", "HEAD"]


@app.route("/", defaults={"path": ""}, methods=methods)
@app.route("/<path:path>", methods=methods)
def redirect_handler(path):
    qs = request.query_string.decode("utf-8")
    new_url = f"{APP_URL}/{path}?{qs}" if path else f"{APP_URL}?{qs}"
    return redirect(new_url, code=301)


if __name__ == "__main__":
    app.run(debug=False)
