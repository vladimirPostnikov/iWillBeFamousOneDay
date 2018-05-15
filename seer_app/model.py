from wtforms import Form, SelectField, validators
from compute import generate_tuples

class SimpleForm(Form):
	
    GENDERS = ('M', 'F')
    gender = SelectField(label ='Gender', choices=[(age, age) for age in GENDERS])
	
    AGE_RANGES = ('18-30', '30-39', '40-49', '50-59', '60-69', '70-79', '80+')	
    age = SelectField(label ='Age', choices=[(ageXD, ageXD) for ageXD in AGE_RANGES])	
	
    Previous_Alcohol_Abuse = ('0','1')
    alcoholabuse = SelectField(label ='Previous Alcohol Abuse', choices=[(age, age) for age in  Previous_Alcohol_Abuse])
	
    Alcohol_Dependence = ('0','1')
    alcoholdependence = SelectField(label ='Alcohol Dependence', choices=[(age, age) for age in  Alcohol_Dependence])
	
    Alcohol_Liver_Disease = ('0','1')
    alcoholliverdisease = SelectField(label ='Acute Alcoholic Hepatitis', choices=[(age, age) for age in  Alcohol_Liver_Disease])
	
