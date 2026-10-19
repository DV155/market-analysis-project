import csv
import io
import os
import sqlite3
import threading
import time
import urllib.request

DATA_URL = "https://data.statistik.gv.at/data/OGD_vpi15_VPI_2015_1.csv"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "austrian_cpi.db")
MAX_AGE_DAYS = 30
updateLock = threading.Lock() # Stops simultaneous requests from all downloading and writing at once

columnNames = {
    "VPI-0": "cpi_overall",
    "VPI-01": "food_beverages",
    "VPI-02": "alcohol_tobacco",
    "VPI-03": "clothing_footwear",
    "VPI-04": "housing_utilities",
    "VPI-05": "furnishings_household",
    "VPI-06": "health",
    "VPI-07": "transport",
    "VPI-08": "communication",
    "VPI-09": "recreation_culture",
    "VPI-10": "education",
    "VPI-11": "restaurants_hotels",
    "VPI-12": "miscellaneous",
}
columns = list(columnNames.values())


def download_csv():
    with urllib.request.urlopen(DATA_URL, timeout=30) as response:
        text = response.read().decode("utf-8")
    return list(csv.DictReader(io.StringIO(text), delimiter=";"))


def build_rows(csvRows):
    yearly = {2015: {column: 100.0 for column in columns}} # Base year, every index is 100 by definition
    for row in csvRows:
        period = row["C-VPIZR-0"].removeprefix("VPIZR-") 
        column = columnNames.get(row["C-VPI5-0"])
        if len(period) != 4 or column is None:
            continue
        yearly.setdefault(int(period), {})[column] = float(row["F-VPIMZBM"].replace(",", "."))

    completeYears = {year: values for year, values in yearly.items() if len(values) == len(columns)}
    if len(completeYears) < 2:
        raise ValueError("No annual CPI data found in the download")
    return completeYears


def build_contributions(csvRows, years):
    contributionRows = []
    for row in csvRows:
        period = row["C-VPIZR-0"].removeprefix("VPIZR-")
        column = columnNames.get(row["C-VPI5-0"])
        if len(period) != 4 or int(period) not in years or column in (None, "cpi_overall"):
            continue
        weight = float(row["F-VPIGEWBM"].replace(",", "."))
        contribution = float(row["F-VPIEFVJM"].replace(",", "."))
        contributionRows.append((int(period), column, weight, contribution))
    return contributionRows


def write_database(yearly, contributionRows): # building a temporary file to avoid half-built db on fail
    tmpPath = DB_PATH.replace(".db", ".tmp.db")
    if os.path.exists(tmpPath):
        os.remove(tmpPath)
    conn = sqlite3.connect(tmpPath)
    columnSql = ", ".join(f"{column} REAL" for column in columns)
    conn.execute(f"CREATE TABLE available_data (year INTEGER PRIMARY KEY, {columnSql})")
    placeholders = ", ".join("?" for _ in range(len(columns) + 1))
    conn.executemany(f"INSERT INTO available_data VALUES ({placeholders})",
                     [[year] + [yearly[year][column] for column in columns] for year in sorted(yearly)])
    conn.execute("CREATE TABLE contributions (year INTEGER, category TEXT, weight REAL, contribution REAL, PRIMARY KEY (year, category))")
    conn.executemany("INSERT INTO contributions VALUES (?, ?, ?, ?)", contributionRows)
    conn.commit()
    conn.close()
    os.replace(tmpPath, DB_PATH)


def database_is_current():
    if not os.path.exists(DB_PATH):
        return False
    ageDays = (time.time() - os.path.getmtime(DB_PATH)) / 86400
    conn = sqlite3.connect(DB_PATH)
    tables = {row[0] for row in conn.execute("SELECT name FROM sqlite_master WHERE type = 'table'")}
    conn.close()
    return ageDays < MAX_AGE_DAYS and {"available_data", "contributions"} <= tables


def update_database(force=False):
    if not force and database_is_current():
        return

    with updateLock:
        if not force and database_is_current(): 
            return
        try:
            csvRows = download_csv()
            yearly = build_rows(csvRows)
            write_database(yearly, build_contributions(csvRows, yearly))
            print(f"CPI data updated: {min(yearly)}-{max(yearly)}")
        except Exception as error:
            if not os.path.exists(DB_PATH):
                raise
            print(f"Could not refresh CPI data ({error}), using the existing database")


if __name__ == "__main__":
    update_database(force=True)
