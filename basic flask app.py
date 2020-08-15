from flask import Flask

app=Flask(__name__)

@app.route("/home")
def index():
    return "Hai preethu from pravalika"

app.run(debug=True)
