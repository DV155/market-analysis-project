from flask import Flask, render_template, request
import sqlite3
import math
#import plotly.express as px
import plotly.graph_objects as go
from datetime import date
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
    dateToday = date.today()
    currentYearCalc = dateToday.year
    currentYear = str(currentYearCalc - 1)
    lastYear = str(currentYearCalc - 2)

    fig = go.Figure(data=go.Scatter(x=years, y=cpi, mode='lines+markers', line=dict(color='#4ade80'), marker=dict(color='#4ade80')))
    config = {'staticPlot': True}
    fig.update_layout(plot_bgcolor='#2d2d2d', paper_bgcolor='#1e1e1e', font=dict(color='#e0e0e0'),xaxis=dict(gridcolor='#444444',tickfont=dict(color='white')),yaxis=dict(gridcolor='#444444',tickfont=dict(color='white')))
    cur.execute(f"SELECT cpi_overall FROM available_data WHERE year = {currentYear}") #Last year inflaton
    currentCPI = cur.fetchone()
    cur.execute(f"SELECT cpi_overall FROM available_data WHERE year = {lastYear}")
    lastYearCPI = cur.fetchone()
    inflationCalc = round(((currentCPI[0] - lastYearCPI[0]) / lastYearCPI[0] ) * 100, 2)

    cur.execute(f"SELECT * from available_data WHERE year = {currentYear}") #Max contributor
    maxValue = cur.fetchone()
    neededValue = max(maxValue[2:])
    column_names = [desc[0] for desc in cur.description]
    max_index = maxValue.index(neededValue) 
    max_column = column_names[max_index]
    clean_name = max_column.title().replace('_', ' and ')

    cur.execute(f"SELECT food_beverages from available_data WHERE year IN ({lastYear}, {currentYear}) ORDER BY year") #The big 3
    foodData = cur.fetchall()
    foodDif = round(((foodData[1][0] - foodData[0][0]) / foodData[0][0] ) * 100, 2)
    cur.execute(f"SELECT education from available_data WHERE year IN ({lastYear}, {currentYear}) ORDER BY year")
    edData = cur.fetchall()
    edDif = round(((edData[1][0] - edData[0][0]) / edData[0][0] ) * 100, 2)
    cur.execute(f"SELECT health from available_data WHERE year IN ({lastYear}, {currentYear}) ORDER BY year")
    healthData = cur.fetchall()
    healthDif = round(((healthData[1][0] - healthData[0][0]) / healthData[0][0] ) * 100, 2)
    conn.close()
    
    graph_html = fig.to_html(full_html=False)
    
    return render_template('index.html', graph=graph_html, lastYear=lastYear, currentYear=currentYear, inflationValue=inflationCalc, neededValue=neededValue, clean_name=clean_name, foodDif=foodDif, edDif=edDif, healthDif=healthDif)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/calc')
def calc():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT year, cpi_overall FROM available_data")

    conn.close()
    return render_template('calculator.html')

if __name__ == "__main__":
    serve(app)