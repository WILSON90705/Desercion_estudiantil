"""
==============================================
ANÁLISIS EXPLORATORIO DE DATOS (EDA)
Proyecto: Deserción Estudiantil
Autor: Wilson
Fecha: 2024
==============================================

Descripción:
    Este script realiza el análisis exploratorio
    del dataset de deserción estudiantil, incluyendo
    limpieza, visualización y análisis estadístico.
"""

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

print(  )

print(df.columns)

print( )

#visualizacion de distribucion de porcewntaje de abandonp
df["Dropout"] = df["Dropout"].astype(int)
# Visualize class distribution
plt.figure(figsize=(6, 4))
sns.countplot(x="Dropout", data=df, palette="Set3")
plt.title("Distribution of Dropout")
plt.xlabel("Dropout")
plt.ylabel("Count")
plt.xticks([0, 1], ["No Dropout", "Dropout"])
plt.show()

print( )    

corr_matrix = df[['Age','Family_Income','Study_Hours_per_Day'
                  ,'Attendance_Rate','Assignment_Delay_Days','Travel_Time_Minutes','GPA']].corr()