# End-to-End ETL Pipeline with Python, Airflow, Spark, Docker, S3, Snowflake & Google Looker Studio

## Introduction
Welcome to this project on building an end-to-end ETL pipeline using Python, Apache Airflow, Spark, Docker, S3, Snowflake, and Google Looker Studio.
In this project, I’ll walk you through the complete process of extracting, transforming, and
visualizing data from YouTube API, all automated with Apache Airflow and deployed in a
Dockerized environment.

## Architecture

![Project Architecture](Project_Architecture.png)

Feel free to analyze the data using various tools.

This dataset contains below columns:

patientunitstayid, patienthealthsystemstayid: Unique Patient Id

Patient Demographics:
gender: Male, Female, Unknown
age
ethnicity

Hospital Details:
hospitalid: Each hospital was given unique id
wardid: Ward Id is given in which patient was treated
apacheadmissiondx: Disease diagnosed
admissionheight: Height of the patients
hospitaladmittime24: Admission time to the hospital
hospitaladmitsource: Department Source of the admission
hospitaldischargeyear: Discharge year from the hospital
hospitaldischargetime24: Discharge time from the hospital
hospitaldischargelocation: Patient Discharge to which location (Home, Death, Other hospital. etc)
hospitaldischargestatus (Alive, Expired)

Hospital Unit Details:
unittype: Unit in which admitted
unitadmittime24: Time of admision to the Unit
unitadmitsource: Department source for the unit
unitvisitnumber: No. of times visited
unitstaytype: Admit, readmit, etc
admissionweight: Weight during the admission
dischargeweight: Weight during the Discharge
unitdischargetime24: Discharge time from the Unit
unitdischargelocation: Patient Discharge to which location (Home, Death, Other hospital. etc)
unitdischargestatus: (Alive, Expired)

Date of admission and discharge is not given in the dataset, you can assume it to be 24 hours data.

I have worked on a dashboard assessing no. of patients admitted, avg. duration of hospital stay, disease condition for which they are admitted etc.

You can also do your analysis. Do share your findings with me. Thanks!
