#modelo Eda
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns



conexion = mysql.connector.connect(
    host="localhost",
    user="root",
    password="WILSONTARRIFA1234",
    database="estudiantes"
)

# Desactivar el modo estricto en esta sesión

cursor = conexion.cursor()
cursor.execute("SET SESSION sql_mode = sys.list_drop(@@SESSION.sql_mode, 'ONLY_FULL_GROUP_BY')")
df = pd.read_sql("SELECT * FROM students1", con=conexion)
df.head()
print(df.head())

print( )
print(df.info())
print( )
print(df.describe())

print()

print(df.isnull().sum())

print()

print()

#valores perdidos
miss =  df.isnull().sum()
miss = miss[miss > 0]

#distribucion de abandonoso
# Class distribution
print("Target Distribution:")
print(df["Dropout"].value_counts())
print(f"\nDropout rate: {df['Dropout'].mean():.1%}")