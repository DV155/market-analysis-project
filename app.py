from flask import Flask, render_template
import sqlite3
import math
import matplotlib.pyplot as plt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///austrian_cpi.db'

conn = sqlite3.connect("austrian_cpi.db")
cur = conn.cursor()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)