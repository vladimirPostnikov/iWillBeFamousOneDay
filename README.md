# HW5-Group-Assignment - CS.601.265 (Spring 2018)

## Team Members

1. Zach Heiman (zheiman1)
2. Vladimir Postnikov (vpostni1)

## Project Name

LiverDie

As an web app developer I want to view the distributions of key feature variables for liver cirrhosis so that I can select relevant features for making a predictive model.

## Access and Running Instructions

Note: GitHub pages were not utlized as we were not made admins. (Would have mentioned this to Eli earlier but did not get to that section of the assignment until 2 hours until the due date) 

"Access our interactive chart [here](vladimirpostnikov.pythonanywhere.com) or download this repository and run `python controller.py` and access this from http://127.0.0.1:5000/." Make sure to update the 1000.csv file paths, found in compute.py, prior to running.

## Design details

### Storyboard

https://docs.google.com/document/d/1yq3JChO_4QgVF27l9aRFbXMPmwDyLZX1SN8TqLItv7k/edit?usp=sharing
Our storyboard is quite different from our chart implementation for this assignment. For this assignment we focused on visualizing features specifically for cirrhosis patients (as there is a large portion of these patients in the MIMIC-III dataset) so that we can identify relevant features for the LiverDie application described in the storyboard.

### Interaction

The interaction embedded in this app allows the user to choose between three features to visualize the distributions (age, gender, and race). Once the user selects the feature, clicking the button generates and prints the chart.

### Data description

The MIMIC-III tables used are diagnoses_icd, admissions, and patients, with the goal of finding patients that were diagnosed with liver cirrhosis, and their age at admission, gender, and ethnicity. Knowing these distributions may help us calibrate our liver cirrhosis prediction models for our final project. 

The individual data used while querying are: subject_id, icd9_code, hadm_id, admittime, dob, gender, ethnicity. 

The 1000 patients were found with the query:

WITH table2 as
(
WITH table1 as 
(
SELECT subject_id, icd9_code, hadm_id
FROM diagnoses_icd
WHERE icd9_code = '5712'
ORDER BY subject_id
)
SELECT a.subject_id, a.icd9_code, b.admittime, ethnicity
FROM table1 a
INNER JOIN admissions b
ON a.hadm_id = b.hadm_id
ORDER BY a.subject_id
)
SELECT a.subject_id, a.icd9_code, a.ethnicity, b.gender, ROUND((cast(a.admittime as date) - cast(b.dob as date))/365.242, 0) AS age
FROM table2 a
INNER JOIN patients b
ON a.subject_id = b.subject_id
ORDER BY a.subject_id

## Development Process

Word done by Vlad:
Creating the query used to get our data.
Roughly half of the coding for the flask application.

Work done by Zach: 
Researching and implementing the seaborn graphs needed to represent our data. 
Roughly half of the coding for the flask application.

Work done together:
Part C of the assignment.

Total time put into this assignment: About 4 hours per team member. 
Most time for Vlad: Working with the Mimic database to get the ideal query (~2h).
Most time for Zach: Working with the seaborn graphs (~1.5h).
  
## Data Source Acknowledgement

* MIMIC-III, a freely accessible critical care database. Johnson AEW, Pollard TJ, Shen L, Lehman L, Feng M, Ghassemi M, Moody B, Szolovits P, Celi LA, and Mark RG. Scientific Data (2016). DOI: 10.1038/sdata.2016.35. Available at: http://www.nature.com/articles/sdata201635

©2018 THE JOHNS HOPKINS UNIVERSITY, ALL RIGHTS RESERVED. BALTIMORE, MARYLAND.
"# iWillBeFamousOneDay" 
"# iWillBeFamousOneDay" 
