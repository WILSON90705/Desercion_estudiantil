import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import pyplot as plt
import sweetviz as sv
from dotenv import load_dotenv
import os
from sklearn.preprocessing import OrdinalEncoder,OneHotEncoder , StandardScaler , MinMaxScaler
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn import set_config
from sklearn.utils import estimator_html_repr
import webbrowser
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report

"""
cargar variables de entorno para la conexion a la base de datos
"""
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

# Visualización de variables numéricas Age vs Family_Income

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
#muestreo de datos por sweetviz como segundo dashboard de analisis de datos
report = sv.analyze(df)
report.show_html('Student_Dropout_Report.html')

print( )

"""
seleccion y extracion de variables
"""
dfA = df.drop(columns=['Student_ID','GPA', 'Semester_GPA'])
print(dfA.shape)

print( )

print(dfA.head())

print( )

#departamentos unicos a que intervienen
print(dfA['Department'].unique())

#convirtiendo todos los datos para que el ML pueda procesarlos
oe = OrdinalEncoder()
ohe = OneHotEncoder(sparse_output=False , drop='first')

print(dfA.sample(2))

print( )

print(dfA['Department'].isna().sum())

print( )

dfA['Semester'] = dfA['Semester'].str.split(expand=True)[1]
dfA['Semester'] = dfA['Semester'].astype(int)

print(dfA['Semester'].sample(2))

X = dfA.drop(columns=['Dropout'])
y = dfA['Dropout']

print(X.sample(2))
print( )
print(y.sample(2))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(X_train.shape)
print(X_test.shape)
print(y_train.shape)
print(y_test.shape)

"""
creacion de columnas transformadas para su preprocesamiento
"""
set_config(display='diagram')

si_trf = ColumnTransformer([
    ('si_age', SimpleImputer(), ['Age']),
    ('si_family_income', SimpleImputer(), ['Family_Income']),
    ('si_study_hours', SimpleImputer(), ['Study_Hours_per_Day']),
    ('si_cgpa', SimpleImputer(), ['CGPA']),
    ('si_stress_index', SimpleImputer(), ['Stress_Index']),
    ('si_parental_education', SimpleImputer(strategy='most_frequent'), ['Parental_Education']),
    ('enc_ohe', OneHotEncoder(sparse_output=False, drop='first'), ['Gender', 'Internet_Access', 'Part_Time_Job', 'Scholarship', 'Department']),
], remainder='passthrough')

si_trf.set_output(transform="pandas")

si_trf

with open("diagrama.html", "w", encoding="utf-8") as f:
    f.write(estimator_html_repr(si_trf))

webbrowser.open("diagrama.html")


enc_trf = ColumnTransformer([
     ('enc_oe',oe,['si_parental_education__Parental_Education'])
],remainder='passthrough')
enc_trf.set_output(transform="pandas")

with open("diagrama2.html", "w", encoding="utf-8") as f:
    f.write(estimator_html_repr(enc_trf))

webbrowser.open("diagrama2.html")

"""
Creación de transformadores de columna para escalado
"""

scale_trf = ColumnTransformer([
    ('scaler',StandardScaler(), slice(0,19))
])

pipe = Pipeline([
     ('si_trf',si_trf),
     ('enc_trf',enc_trf),
    ('scale_trf',scale_trf),
    ('model',LogisticRegression()) # Added a solver for good practice
     #('model',DecisionTreeClassifier(max_depth=10))
     #('model',SVC(kernel='linear'))
     #('model',RandomForestClassifier())
])

pipe.fit(X_train,y_train)

with open("diagrama3.html", "w", encoding="utf-8") as f:
    f.write(estimator_html_repr(pipe))

webbrowser.open("diagrama3.html")

y_pred = pipe.predict(X_test)


print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))