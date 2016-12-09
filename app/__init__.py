from flask import Flask

app=Flask(__name__)
app.debug=True
app.config["SECRET_KEY"]="233333asd"

from app import views