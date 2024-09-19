import pandas as pd
import mysql.connector


db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="contrseña",
    database="base_datos_sistemos_op"
)

cursor = db.cursor()

df = pd.read_csv('results.csv')


for _, row in df.iterrows():
    sql = "INSERT INTO partidos (home_team, away_team, home_goals, away_goals, result, season) VALUES (%s, %s, %s,%s,%s,%s)"
    cursor.execute(sql, tuple(row))

db.commit()

cursor.close()
db.close()
