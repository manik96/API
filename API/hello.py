#Archivo de pruebas para corroborar el estado del ambiente de trabajo

from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

