from flask import Flask, render_template, request
import sqlite3
import math
#import plotly.express as px
import plotly.graph_objects as go
from waitress import serve
from fetch_data import update_database, DB_PATH

app = Flask(__name__)
categoryNamesDE = {
    "food_beverages": "Nahrungsmittel und alkoholfreie Getränke",
    "alcohol_tobacco": "Alkoholische Getränke und Tabak",
    "clothing_footwear": "Bekleidung und Schuhe",
    "housing_utilities": "Wohnung, Wasser, Energie",
    "furnishings_household": "Hausrat und laufende Instandhaltung",
    "health": "Gesundheit",
    "transport": "Verkehr",
    "communication": "Nachrichtenübermittlung",
    "recreation_culture": "Freizeit und Kultur",
    "education": "Erziehung und Unterricht",
    "restaurants_hotels": "Restaurants und Hotels",
    "miscellaneous": "Verschiedene Waren und Dienstleistungen",
}
def get_db_connection():
    update_database() # Downloads the CPI data if the DB is missing or older than 30 days
    conn = sqlite3.connect(DB_PATH)
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT year, cpi_overall FROM available_data")
    data = cur.fetchall()

    years = [row[0] for row in data]
    cpi = [row[1] for row in data]
    cur.execute("SELECT MAX(year) FROM available_data") #Latest year in the DB
    currentYearCalc = cur.fetchone()[0]
    currentYear = str(currentYearCalc)
    lastYear = str(currentYearCalc - 1)

    fig = go.Figure(data=go.Scatter(x=years, y=cpi, mode='lines+markers', line=dict(color='#34c759', width=3), marker=dict(color='#34c759', size=7)))
    config = {'staticPlot': True}
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family='-apple-system, BlinkMacSystemFont, system-ui, Segoe UI, Roboto, sans-serif', color='#8e8e93'), margin=dict(l=56, r=24, t=16, b=48), xaxis=dict(title='Year',showgrid=False,linecolor='rgba(142,142,147,0.4)',tickfont=dict(color='#8e8e93')),yaxis=dict(title='CPI (2015 = 100)',gridcolor='rgba(142,142,147,0.2)',zeroline=False,tickfont=dict(color='#8e8e93')))
    cur.execute(f"SELECT cpi_overall FROM available_data WHERE year = {currentYear}") 
    currentCPI = cur.fetchone()
    cur.execute(f"SELECT cpi_overall FROM available_data WHERE year = {lastYear}")
    lastYearCPI = cur.fetchone()
    inflationCalc = round(((currentCPI[0] - lastYearCPI[0]) / lastYearCPI[0] ) * 100, 2)

    cur.execute("SELECT category, contribution FROM contributions WHERE year = ? ORDER BY contribution DESC LIMIT 1", (currentYearCalc,)) #Max contributor in percentage points
    max_column, neededValue = cur.fetchone()
    neededValue = round(neededValue, 2)
    clean_name = max_column.title().replace('_', ' and ')

    cur.execute(f"SELECT food_beverages from available_data WHERE year IN ({lastYear}, {currentYear}) ORDER BY year") 
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

@app.route('/de')
def indexDE():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT year, cpi_overall FROM available_data")
    data = cur.fetchall()

    years = [row[0] for row in data]
    cpi = [row[1] for row in data]
    cur.execute("SELECT MAX(year) FROM available_data") #Latest year in the DB
    currentYearCalc = cur.fetchone()[0]
    currentYear = str(currentYearCalc)
    lastYear = str(currentYearCalc - 1)

    fig = go.Figure(data=go.Scatter(x=years, y=cpi, mode='lines+markers', line=dict(color='#34c759', width=3), marker=dict(color='#34c759', size=7)))
    config = {'staticPlot': True}
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(family='-apple-system, BlinkMacSystemFont, system-ui, Segoe UI, Roboto, sans-serif', color='#8e8e93'), margin=dict(l=56, r=24, t=16, b=48), xaxis=dict(title='Jahr',showgrid=False,linecolor='rgba(142,142,147,0.4)',tickfont=dict(color='#8e8e93')),yaxis=dict(title='VPI (2015 = 100)',gridcolor='rgba(142,142,147,0.2)',zeroline=False,tickfont=dict(color='#8e8e93')))
    cur.execute(f"SELECT cpi_overall FROM available_data WHERE year = {currentYear}") #Last year inflaton
    currentCPI = cur.fetchone()
    cur.execute(f"SELECT cpi_overall FROM available_data WHERE year = {lastYear}")
    lastYearCPI = cur.fetchone()
    inflationCalc = round(((currentCPI[0] - lastYearCPI[0]) / lastYearCPI[0] ) * 100, 2)

    cur.execute("SELECT category, contribution FROM contributions WHERE year = ? ORDER BY contribution DESC LIMIT 1", (currentYearCalc,)) #Max contributor in percentage points
    max_column, neededValue = cur.fetchone()
    neededValue = round(neededValue, 2)
    clean_name = categoryNamesDE[max_column]

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
    
    return render_template('indexDE.html', graph=graph_html, lastYear=lastYear, currentYear=currentYear, inflationValue=inflationCalc, neededValue=neededValue, clean_name=clean_name, foodDif=foodDif, edDif=edDif, healthDif=healthDif)


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/aboutDE')
def aboutDE():
    return render_template('aboutDE.html')

def get_calc_values():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT year, cpi_overall FROM available_data")
    cpiData = dict(cur.fetchall())
    conn.close()

    latestYear = max(cpiData)
    baseYear = latestYear - 10
    if baseYear not in cpiData: # Fall back to 2015 if there's no data from ten years ago
        baseYear = 2015
    priceFactor = cpiData[latestYear] / cpiData[baseYear]
    purchasingLoss = round((1 - cpiData[baseYear] / cpiData[latestYear]) * 100, 1)
    return dict(baseYear=baseYear, latestYear=latestYear, yearSpan=latestYear - baseYear, priceFactor=priceFactor, purchasingLoss=purchasingLoss)

@app.route('/calc')
def calc():
    return render_template('calculator.html', **get_calc_values())

@app.route('/calcDE')
def calcDE():
    return render_template('calculatorDE.html', **get_calc_values())

if __name__ == "__main__":
    #serve(app)
    app.run(debug=True)