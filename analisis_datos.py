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
from matplotlib import pyplot as plt
import sweetviz as sv

from dotenv import load_dotenv
import os

load_dotenv("C:/Users/wilso/Desktop/x/x/python/analisis de datos/tablas 2/variables.env")

conexion = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
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
sns.countplot(x="Dropout", data=df, hue="Dropout", palette="Set3", legend=False)
plt.title("Distribution of Dropout")
plt.xlabel("Dropout")
plt.ylabel("Count")
plt.xticks([0, 1], ["No Dropout", "Dropout"])
plt.show()

print( )    

corr_matrix = df[['Age','Family_Income','Study_Hours_per_Day'
                  ,'Attendance_Rate','Assignment_Delay_Days','Travel_Time_Minutes','GPA']].corr()

plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
plt.title('Correlation Matrix')
plt.show()

print( )


#for column in df.columns:
#    if df[column].dtype == 'object':
#        plt.figure(figsize=(8, 4))
#        sns.countplot(x=column, data=df, palette="Set2")
#        plt.title(f'Distribution of {column}')
#        plt.xticks(rotation=45)
#        plt.show()


for column in ['Age', 'Family_Income']:
    plt.figure(figsize=(8, 4))
    sns.histplot(df[column], kde=True, color='blue')
    plt.title(f'Distribution of {column}')
    plt.xlabel(column)
    plt.ylabel('Frequency')
    plt.show()


#for column in ['Study_Hours_per_Day', 'Attendance_Rate', 'Assignment_Delay_Days', 'Travel_Time_Minutes']:
#    plt.figure(figsize=(8, 4))
#    sns.histplot(df[column], kde=True, color='green')
#    plt.title(f'Distribution of {column}')
#    plt.xlabel(column)
#    plt.ylabel('Frequency')
#    plt.show()

#for column in ['GPA']:
#    plt.figure(figsize=(8, 4))
#    sns.histplot(df[column], kde=True, color='red')
#    plt.title(f'Distribution of {column}')
#    plt.xlabel(column)
#    plt.ylabel('Frequency')
#    plt.show()

print( )

report = sv.analyze(df)
report.show_html('Student_Dropout_Report.html')