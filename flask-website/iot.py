from flask import Flask, g, render_template

app = Flask(__name__)

@app.route('/')
def main_page():
    return '<3'

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
