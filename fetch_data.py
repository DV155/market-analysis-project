import csv
import io
import os
import sqlite3
import time
import urllib.request

# Consumer Price Index base 2015 from Statistik Austria's open data portal (CC BY 4.0)
DATA_URL = "https://data.statistik.gv.at/data/OGD_vpi15_VPI_2015_1.csv"
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "austrian_cpi.db")
MAX_AGE_DAYS = 30

# Statistik Austria COICOP codes -> columns in available_data
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
        period = row["C-VPIZR-0"].removeprefix("VPIZR-") # "2025" = annual average, "202512" = single month
        column = columnNames.get(row["C-VPI5-0"])
        if len(period) != 4 or column is None:
            continue
        yearly.setdefault(int(period), {})[column] = float(row["F-VPIMZBM"].replace(",", "."))

    completeYears = {year: values for year, values in yearly.items() if len(values) == len(columns)}
    if len(completeYears) < 2:
        raise ValueError("No annual CPI data found in the download")
    return completeYears


def write_database(yearly):
    # Build into a temporary file first so a failed run never leaves a half-written database
    tmpPath = DB_PATH.replace(".db", ".tmp.db")
    if os.path.exists(tmpPath):
        os.remove(tmpPath)
    conn = sqlite3.connect(tmpPath)
    columnSql = ", ".join(f"{column} REAL" for column in columns)
    conn.execute(f"CREATE TABLE available_data (year INTEGER PRIMARY KEY, {columnSql})")
    placeholders = ", ".join("?" for _ in range(len(columns) + 1))
    conn.executemany(f"INSERT INTO available_data VALUES ({placeholders})",
                     [[year] + [yearly[year][column] for column in columns] for year in sorted(yearly)])
    conn.commit()
    conn.close()
    os.replace(tmpPath, DB_PATH)


def update_database(force=False):
    if not force and os.path.exists(DB_PATH):
        ageDays = (time.time() - os.path.getmtime(DB_PATH)) / 86400
        if ageDays < MAX_AGE_DAYS:
            return

    try:
        yearly = build_rows(download_csv())
        write_database(yearly)
        print(f"CPI data updated: {min(yearly)}-{max(yearly)}")
    except Exception as error:
        if not os.path.exists(DB_PATH):
            raise
        print(f"Could not refresh CPI data ({error}), using the existing database")


if __name__ == "__main__":
    update_database(force=True)
