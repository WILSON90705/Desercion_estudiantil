import pandas as pd
import mysql.connector

conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="WILSONTARRIFA1234",
    database="estudiantes"
)

df = pd.read_sql("SELECT * FROM V_MODELO_FINAL", con=conexion)
df.head()
print(df.head())
