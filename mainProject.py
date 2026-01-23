import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("austrian_cpi.db")
cur = conn.cursor()

desFactor = input("What basket component do you want?")
desYear = input("What year do you want?")
validFactors = ["cpi_overall", "food_beverages", "alcohol_tobacco", "clothing_footwear", "housing_utilities", "furnishings_household",	"health", "transport", "communication", "recreation_culture", "education", "restaurants_hotels", "miscellaneous"]
if desFactor in validFactors:
    cur.execute(f"SELECT {desFactor} FROM available_data WHERE year = (?)", (desYear,))
    result = cur.fetchone()
    print(result[0])
else:
    print("Invalid querry")
cur.execute("SELECT cpi_overall FROM available_data WHERE year = 2025")
currentCPI = cur.fetchone()
print("2025 Austrian CPI is", currentCPI[0])
maxValue = max(result[1:])
print("Highest CPI contributor in 2025 is at", maxValue)
