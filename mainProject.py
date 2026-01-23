import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("austrian_cpi.db")
cur = conn.cursor()

cur.execute("SELECT * FROM available_data")
result = cur.fetchall()
for column in result:
    print(column)