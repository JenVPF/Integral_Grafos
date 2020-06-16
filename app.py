from flask import Flask, render_template
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/datos', methods=['GET', 'POST'])
def datos():
    return render_template("datos.html")

if __name__ == '__main__':
    app.run(debug=True)