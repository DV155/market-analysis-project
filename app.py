from flask import Flask, render_template, request
import sqlite3
import math
#import plotly.express as px
import plotly.graph_objects as go
from waitress import serve

app = Flask(__name__)
def get_db_connection():
    conn = sqlite3.connect('austrian_cpi.db')
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT year, cpi_overall FROM available_data")
    data = cur.fetchall()

    years = [row[0] for row in data]
    cpi = [row[1] for row in data]

    fig = go.Figure(data=go.Scatter(x=years, y=cpi, mode='lines+markers'))
    config = {'staticPlot': True}
    cur.execute("SELECT cpi_overall FROM available_data WHERE year = 2025")
    currentCPI = cur.fetchone()
    cur.execute("SELECT cpi_overall FROM available_data WHERE year = 2024")
    lastYearCPI = cur.fetchone()
    inflationCalc = round(((currentCPI[0] - lastYearCPI[0]) / lastYearCPI[0] ) * 100, 2)
    conn.close()
    
    graph_html = fig.to_html(full_html=False)
    
    return render_template('index.html', graph=graph_html, inflationValue=inflationCalc)

if __name__ == "__main__":
    serve(app)