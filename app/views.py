from app import app
from flask import render_template
from datetime import datetime, timedelta


@app.route("/")
@app.route("/index")
def index():
    return render_template(
        "index.html",
        today=get_date()
    )


def get_date():
    return datetime.now().strftime("%c")
