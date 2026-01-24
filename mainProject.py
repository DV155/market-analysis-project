import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import math

conn = sqlite3.connect("austrian_cpi.db")
cur = conn.cursor()

cur.execute("SELECT cpi_overall FROM available_data WHERE year = 2025")
currentCPI = cur.fetchone()
print("2025 Austrian CPI is", currentCPI[0])
cur.execute("SELECT cpi_overall FROM available_data WHERE year = 2024")
lastYearCPI = cur.fetchone()
inflationCalc = round(((currentCPI[0] - lastYearCPI[0]) / lastYearCPI[0] ) * 100, 2)
print("This means a", inflationCalc, "% inflation rate from 2024 to 2025")
cur.execute("SELECT * from available_data WHERE year = 2025")
maxValue = cur.fetchone()
neededValue = max(maxValue[2:])
column_names = [desc[0] for desc in cur.description]
max_index = maxValue.index(neededValue) 
max_column = column_names[max_index]
print("Biggest contributor in 2025 is " + max_column + " at " +  str(neededValue))
desFactor = input("What basket component do you want?")
desYear = input("What year do you want?")
validFactors = ["cpi_overall", "food_beverages", "alcohol_tobacco", "clothing_footwear", "housing_utilities", "furnishings_household",	"health", "transport", "communication", "recreation_culture", "education", "restaurants_hotels", "miscellaneous"]
if desFactor in validFactors:
    cur.execute(f"SELECT {desFactor} FROM available_data WHERE year = (?)", (desYear,))
    result = cur.fetchone()
    print(result[0])
else:
    print("Invalid querry")
