import sqlite3
import matplotlib.pyplot as plt
import math
from fetch_data import update_database, DB_PATH

update_database() # Downloads the CPI data if the DB is missing or older than 30 days
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("SELECT MIN(year), MAX(year) FROM available_data")
firstYear, currentYear = cur.fetchone()
lastYear = currentYear - 1

cur.execute("SELECT cpi_overall FROM available_data WHERE year = ?", (currentYear,))
currentCPI = cur.fetchone()
print(currentYear, "Austrian CPI is", currentCPI[0])
cur.execute("SELECT cpi_overall FROM available_data WHERE year = ?", (lastYear,))
lastYearCPI = cur.fetchone()
inflationCalc = round(((currentCPI[0] - lastYearCPI[0]) / lastYearCPI[0] ) * 100, 2)
print("This means a", inflationCalc, "% inflation rate from", lastYear, "to", currentYear)
cur.execute("SELECT category, contribution FROM contributions WHERE year = ? ORDER BY contribution DESC LIMIT 1", (currentYear,))
max_column, neededValue = cur.fetchone()
print("Biggest contributor in " + str(currentYear) + " is " + max_column + " at " +  str(neededValue) + " percentage points")
desFactor = input("What basket component do you want?")
desYear = input("What year do you want?")
validFactors = ["cpi_overall", "food_beverages", "alcohol_tobacco", "clothing_footwear", "housing_utilities", "furnishings_household",	"health", "transport", "communication", "recreation_culture", "education", "restaurants_hotels", "miscellaneous"]
if desFactor in validFactors:
    cur.execute(f"SELECT {desFactor} FROM available_data WHERE year = (?)", (desYear,))
    result = cur.fetchone()
    print(result[0])
else:
    print("Invalid querry")
cur.execute("SELECT year from available_data")
allYears = cur.fetchall()
cur.execute("SELECT cpi_overall from available_data")
allCPIs = cur.fetchall()
x = allYears
y = allCPIs

plt.plot(x, y, marker="o")
plt.title(f'Austrian CPI {firstYear}-{currentYear}')
plt.xlabel('Year')
plt.ylabel('Overall CPI')
ax = plt.gca()
ax.set_xlim([firstYear, currentYear])
ax.set_ylim([min(allCPIs)[0] - 5, max(allCPIs)[0] + 5])
plt.show()