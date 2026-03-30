use estudiantes;
/*select * from student_dropout_dataset_v3;*/
alter view Maximos AS
SELECT Min(Student_ID) AS student_id,
       Min(Age) As Age_id,
       Min(Gender) As gender_id,
       MIN(Family_Income) as Family_Income_id,
       MIN(Internet_Access) as Internet_Access_id,
       MIN(Study_Hours_per_Day) AS Study_Hours_per_Day_id,
       MIN(Attendance_Rate) As Attendance_Rate_id,
       MIN(Assignment_Delay_Days) As Assignment_Delay_Days_id,
	   MIN(Travel_Time_Minutes) As Travel_Time_Minutes_id,
       MIN(Part_Time_job) As Part_Time_job_id,
       MIN(Scholarship) As Scholarship_id,
       MIN(Stress_index) As Stress_index_id,
       MIN(GPA) AS GPA_id,
       MIN(Semester_GPA) As Semester_GPA_id,
       MIN(CGPA) As CGPA_id,
       Min(Semester) As Semester_id,
       MIN(Department) As Department_id,
       MIN(Parental_Education) As Parent_Education_id,
       MIN(Dropout) As Dropout_id
FROM students1
UNION
SELECT MAX(Student_ID),MAX(Age),
       MAX(Gender),MAX(Family_Income),
	   MAX(Internet_Access),MAX(Study_Hours_per_Day),
       MAX(Attendance_Rate),MAX(Assignment_Delay_Days),
       MAX(Travel_Time_Minutes),MAX(Part_Time_job),
       MAX(Scholarship),MAX(Stress_index),
       MAX(GPA),MAX(Semester_GPA),MAX(CGPA),MAX(Semester),
       MAX(Department), MAX(Parental_Education),MAX(Dropout)
FROM students1; 
ALTER VIEW COLUMNAS_Numericas AS
SELECT 
    Student_ID AS Numeric1,
    Age AS Numeric2,
    Family_Income AS Numeric3,
    Study_Hours_per_Day AS Numeric4,
    Attendance_Rate As Numeric5,
    Assignment_Delay_Days As Numeric6,
    Travel_Time_Minutes As Numeric7,
    Stress_Index As Numeric8,
    GPA As Numeric9,
    Semester_GPA As Numeric10,
    CGPA AS Numeric11,
    Dropout As Numeric12
FROM students1
GROUP BY Numeric1, Numeric2, Numeric3, Numeric4, Numeric5,
         Numeric6,Numeric7,Numeric8,Numeric9,Numeric10,
         Numeric11,Numeric12;
         
ALTER view VENTANA_CATEGORICA AS
SELECT
      Gender As Categorical_col1,
      Internet_Access As Categorical_col2,
      Part_Time_job As Categorical_col3,
      scholarship As Categorical_col4,
      Semester As Categorical_col5,
      Department As Categorical_col6,
      Parental_Education As Categorical_col7
	  FROM students1
GROUP BY Categorical_col1,Categorical_col2,Categorical_col3,
         Categorical_col4,Categorical_col5,Categorical_col6,
		 Categorical_col7;


CREATE OR REPLACE VIEW CONTEO AS

-- COUNT
SELECT 
    'count' AS metric,
    COUNT(Student_ID) AS Student_ID,
    COUNT(Age) AS Age,
    COUNT(Family_Income) AS Family_Income,
    COUNT(Study_Hours_per_Day) AS Study_Hours_per_Day,
    COUNT(Attendance_Rate) AS Attendance_Rate,
    COUNT(Assignment_Delay_Days) AS Assignment_Delay_Days,
    COUNT(Travel_Time_Minutes) AS Travel_Time_Minutes,
    COUNT(Stress_Index) AS Stress_Index,
    COUNT(GPA) AS GPA,
    COUNT(Semester_GPA) AS Semester_GPA,
    COUNT(CGPA) AS CGPA,
    COUNT(Dropout) AS Dropout
FROM students1

UNION ALL

-- MEAN
SELECT 
    'mean',
    AVG(Student_ID),
    AVG(Age),
    AVG(Family_Income),
    AVG(Study_Hours_per_Day),
    AVG(Attendance_Rate),
    AVG(Assignment_Delay_Days),
    AVG(Travel_Time_Minutes),
    AVG(Stress_Index),
    AVG(GPA),
    AVG(Semester_GPA),
    AVG(CGPA),
    AVG(Dropout)
FROM students1

UNION ALL

-- STD
SELECT 
    'std',
    STDDEV_SAMP(Student_ID),
    STDDEV_SAMP(Age),
    STDDEV_SAMP(Family_Income),
    STDDEV_SAMP(Study_Hours_per_Day),
    STDDEV_SAMP(Attendance_Rate),
    STDDEV_SAMP(Assignment_Delay_Days),
    STDDEV_SAMP(Travel_Time_Minutes),
    STDDEV_SAMP(Stress_Index),
    STDDEV_SAMP(GPA),
    STDDEV_SAMP(Semester_GPA),
    STDDEV_SAMP(CGPA),
    STDDEV_SAMP(Dropout)
FROM students1

UNION ALL

-- MIN
SELECT 
    'min',
    MIN(Student_ID),
    MIN(Age),
    MIN(Family_Income),
    MIN(Study_Hours_per_Day),
    MIN(Attendance_Rate),
    MIN(Assignment_Delay_Days),
    MIN(Travel_Time_Minutes),
    MIN(Stress_Index),
    MIN(GPA),
    MIN(Semester_GPA),
    MIN(CGPA),
    MIN(Dropout)
FROM students1

UNION ALL

-- MAX
SELECT 
    'max',
    MAX(Student_ID),
    MAX(Age),
    MAX(Family_Income),
    MAX(Study_Hours_per_Day),
    MAX(Attendance_Rate),
    MAX(Assignment_Delay_Days),
    MAX(Travel_Time_Minutes),
    MAX(Stress_Index),
    MAX(GPA),
    MAX(Semester_GPA),
    MAX(CGPA),
    MAX(Dropout)
FROM students1;



/*select * from maximos;
select * from COLUMNAS_NUMERICAS;
select * FROM  VENTANA_CATEGORICA;
select * from conteo; 
select * from EDA;
*/
-- grafico de EDA
alter VIEW EDA AS
SELECT Student_ID AS estudiantes,
    Age AS Age_grafico,
    COUNT(*) AS c
FROM students1
GROUP BY Age;

-- =============================================
-- Vista: Riesgo de desercion
-- Descripción: Consolida el riesgo de deserción basado en el r
-- Tablas: numero_de_estudiantes,ingreso_familiar,conteo-de-abandono 
-- Autor: Wilson Tarrifa
-- Fecha: 2026-03-26
-- =============================================

-- riesgo de desercion
alter view  riesgo_por_edad AS
SELECT Student_ID as estudiantes,
    Age as edad,
    COUNT(*) AS total_dropout,
    ROUND(COUNT(*) * 100.0 /
        (SELECT COUNT(*) 
         FROM students1 s2 
         WHERE s2.Age = s1.Age),2) AS riesgo_porcentaje
FROM students1 s1
WHERE Dropout = 'Yes'
GROUP BY edad
ORDER BY riesgo_porcentaje DESC;



-- =============================================
-- Vista: Riesgo academico
-- Descripción: Consolida el riesgo de deserción basado en el ingreso familiar
-- Tablas: numero_de_estudiantes,ingreso_familiar,conteo-de-abandono 
-- Autor: Wilson Tarrifa
-- Fecha: 2026-03-26
-- =============================================

-- Riesgo academico
ALTER VIEW Riesgo_Academico AS
SELECT Student_ID AS estudiantes,
    Gender as genero,
    Department as departamento,
    AVG(GPA) AS promedio_gpa,
    AVG(CGPA) AS promedio_cgpa,
    AVG(Semester_GPA) AS promedio_semestre,
    AVG(Attendance_Rate) AS promedio_asistencia,
    AVG(Study_Hours_per_Day) AS horas_estudio_diarias,
    AVG(Assignment_Delay_Days) AS promedio_retraso_tareas,
    AVG(Stress_Index) AS promedio_estres,
    Semester As semester,
    COUNT(*) AS total_estudiantes,
    SUM(CASE WHEN Dropout = 1 THEN 1 ELSE 0 END) AS total_desercion
FROM students1
GROUP BY estudiantes, genero, departamento;  -- ✅ estudiantes primero


-- =============================================
-- Vista: Riesgo por ingreso familiar
-- Descripción: Consolida el riesgo de deserción basado en el ingreso familiar
-- Tablas: numero_de_estudiantes,ingreso_familiar,conteo-de-abandono 
-- Autor: Wilson Tarrifa
-- Fecha: 2026-03-26
-- =============================================

-- riesgo por ingreso familiar 
alter VIEW riesgo_ingreso_familiar AS
SELECT Student_ID as estudiantes,
    Family_Income AS ingreso_familia, 
    COUNT(*) AS total_Dropout
FROM students1
WHERE Dropout = 'yes'
GROUP BY estudiantes, ingreso_familia;

-- =============================================
-- Vista: Perfil socioeconómico
-- Descripción: Consolida el perfil socioeconómico de los estudiantes
-- Tablas: numero_de_estudiantes,ingreso_familiar,acceso_internet
-- Autor: Wilson Tarrifa
-- Fecha: 2026-03-26
-- =============================================

-- perfil_socioeconomico
alter VIEW perfil_socioeconomico AS
SELECT  Student_ID AS estudiantes,
    Family_Income AS ingreso_familiar,
    Internet_Access As acceso_internet,
    COUNT(*) AS total_students
FROM students1
GROUP BY estudiantes,ingreso_familiar,acceso_internet;

-- =============================================
-- Vista: Comportamiento
-- Descripción: Consolida comportamiento académico y social de los estudiantes
-- Tablas: numero_de_estudiantes,promedio general, beca, indice_estres, indice_asistencia, 
-- condicion_trabajo, abandono, horas_estudio, acceso_internet, tiempo_viaje
-- Autor: Wilson Tarrifa
-- Fecha: 2026-03-26
-- =============================================

alter view Comportamiento As 
SELECT Student_ID As estudiantes,
      AVG(GPA) AS promedio_gpa,
      Scholarship AS beca,
      Stress_Index AS indice_estress,
      AVG(Attendance_Rate) AS indice_asistencia,
      Part_Time_Job AS condicion_trabajo,
      Dropout AS abandono,
      Study_Hours_per_Day AS horas_estudio,
      Internet_Access AS acceso_internet,
      Travel_Time_Minutes AS tiempo_viaje
FROM students1
GROUP BY
      estudiantes,
      indice_estress,
      beca,
      condicion_trabajo,
      abandono,
      horas_estudio,
      acceso_internet,
      Tiempo_viaje;
      
      


ALTER VIEW Rendimiento AS
SELECT 
      Student_ID AS estudiantes,
      Semester AS semestre,
      AVG(CGPA) AS promedio_total_carrera,
      AVG(GPA) AS promedio_general,
      AVG(Semester_GPA) AS promedio_semestral
FROM students1
GROUP BY Student_ID, Semester;  --  agupaciones por nombre de columna

-- =============================================
-- Vista: V_MODELO_FINAL
-- Descripción: Consolida riesgo académico,
--              rendimiento y perfil socioeconómico
-- Tablas: Riesgo_Academico, Rendimiento,
--         Perfil_socioeconomico, Comportamiento
-- Autor: Wilson Tarrifa
-- Fecha: 2026-03-26
-- =============================================

ALTER VIEW V_MODELO_FINAL AS
WITH 
riesgo AS (SELECT * FROM Riesgo_Academico),
rendimiento AS (SELECT * FROM Rendimiento),
socio AS (SELECT * FROM Perfil_socioeconomico),
comportamiento AS (SELECT * FROM Comportamiento)
SELECT 
    r.estudiantes,
    re.semestre,            -- alias semestre y demas
    re.promedio_general,
    re.promedio_total_carrera,
    re.promedio_semestral,  -- minúscula
    s.ingreso_familiar,
    s.acceso_internet,
    c.indice_estress,
    c.abandono,
    c.horas_estudio,
    c.condicion_trabajo
FROM riesgo r
JOIN rendimiento re USING (estudiantes)
JOIN socio s USING (estudiantes)
JOIN comportamiento c USING (estudiantes);

SET SESSION sql_mode = '';
SELECT * FROM V_MODELO_FINAL;

select * from V_MODELO_FINAL;
 