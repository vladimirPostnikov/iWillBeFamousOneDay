import matplotlib.pyplot as plt
import os, time, glob
import pandas as pd
import numpy as np
import pandas.api.types as ptypes
import seaborn as sns
from sklearn.neighbors import KNeighborsRegressor

# import data file
def data_import(filename):
    patients = pd.read_csv(filename)
    return(patients)

# create tuples of continuous and categorical variables
def generate_tuples():
    self = data_import('1000.csv')

    x_tuple = ()
    y_tuple = ()
    x_tuples = []
    y_tuples = []
    for col in self:
        if col not in ['subject_id', 'icd9_code']:
            typ = ptypes.infer_dtype(self[col])
            if typ == "integer":
                x_tuple = (col,col)
                x_tuples.append(x_tuple) # continuous variables
            elif typ == "string":
                x_tuple = (col,col)
                x_tuples.append(x_tuple) # categorical variables
    tuples = [x_tuples]
    return(tuples)

# values needed for box plot
def compute_metrics(x,yaxis):
   result = {'MIN': x[yaxis].min(), 'MAX': x[yaxis].max(),'MEDIAN': x[yaxis].median(), 'MEAN': x[yaxis].mean()}
   return pd.Series(result, name='metrics')
def kNN(column, data, neighs):
    
    #get training data
    X_train = data.drop(column,1).astype(int)
    y_train = data[column].astype(int)
    
    #create, train model
    classifier = KNeighborsRegressor(n_neighbors=neighs)
    classifier.fit(X_train, y_train)
    return classifier


def train_model():

	#import csv files
    pos_data = pd.read_csv('WithCirrhosis.csv', low_memory=False)
    neg_data = pd.read_csv('WithoutCirrhosis.csv', low_memory=False)
	
	#create indicator variables for cirrhosis
    pos_data['cirrhosis'] = 1
    neg_data['cirrhosis'] = 0
	
	#combine datasets, replace strings with indicator variables
    all_data = neg_data.append(pos_data)
    all_data = all_data.drop('hadm_id',1)
    all_data = all_data.drop('subject_id', 1)
    all_data = all_data.drop('ethnicity', 1)
    all_data[['alcoholabuse', 'alcoholdependence', 'alcoholicliverdisease']] = \
		all_data[['alcoholabuse', 'alcoholdependence', 'alcoholicliverdisease']].replace( \
		np.nan, 0, regex=True)
    all_data[['alcoholabuse', 'alcoholdependence', 'alcoholicliverdisease']] = \
		all_data[['alcoholabuse', 'alcoholdependence', 'alcoholicliverdisease']].replace( \
		'Present', 1, regex=True)
    all_data['gender'] = all_data['gender'].replace('F', 0)
    all_data['gender'] = all_data['gender'].replace('M', 1)
	

	

	
	#replace ages with age ranges 
    for i in range(18,30):
        all_data['age'] = all_data['age'].replace(i, 0)
    for i in range(30,40):
        all_data['age'] = all_data['age'].replace(i, 1)
    for i in range(40,50):
        all_data['age'] = all_data['age'].replace(i, 2)
    for i in range(50,60):
        all_data['age'] = all_data['age'].replace(i, 3)
    for i in range(60,70):
        all_data['age'] = all_data['age'].replace(i, 4)
    for i in range(80,110):
        all_data['age'] = all_data['age'].replace(i, 5)
	
	
    classifier = kNN('cirrhosis', all_data, 8)
    return classifier
	
# create box plot
def plot(gender, age_range, abuse, liver_disease, dependence): # classifier):
    
    classifier = train_model()
    if (gender.data == 'M'):
        gender = 1;
    else:
        gender = 0;
		
    if age_range[0] == '1':
        age_range = 0
    elif age_range[0] == '3':
        age_range = 1
    elif age_range[0] == '4':
        age_range = 2
    elif age_range[0] == '5':
        age_range = 3
    elif age_range[0] == '6':
        age_range = 4
    elif age_range[0] == '7':
        age_range = 5
    elif age_range[0] == '8':
        age_range = 6
    x = {'age': age_range, 'gender': gender, 'alcoholabuse': abuse.data, \
		'alcoholdependence': dependence.data, 'alcoholicliverdisease': liver_disease.data}
    x_pred = pd.DataFrame(data=x, index = [0])
    y_pred = classifier.predict(x_pred)
    print('\n\n\n\n**************\n\n\n\n')
    print(y_pred)
    plt.figure()
    sns.set_style("whitegrid")
	
    level_of_risk = 0
    distance = 0.2
    risk_levels = ['Probability of Cirrhosis: Low', 'Probability of Cirrhosis: Medium', 'Probability of Cirrhosis: High']
    labels = 'Cirrhosis Risk: ' + str((int) (y_pred * 100)) + '%',''
    explode = (.1, 0)  
    if y_pred <= 0.01: y_pred = 0
	
	
    if y_pred <= 0.25: 
        level_of_risk = 0
        distance = 0.5
    elif y_pred > 0.25 and y_pred <= 0.5:
        level_of_risk = 1
    elif y_pred > 0.5 and y_pred <= 1: level_of_risk = 2 
	
    titlefont = {'fontname':'Lato'}
    piefont = {'fontname':'Lato'}
    textprops={'fontsize': 15, 'fontweight': 'bold'}

    plt.title(risk_levels[level_of_risk], fontsize=20, fontweight='bold', **titlefont,)
    y_df = pd.DataFrame({'y':y_pred}, index = [0])
    ax = plt.pie([y_pred, (1-y_pred)], textprops=textprops, explode=explode, labeldistance=distance,shadow=True, labels = labels, startangle=90, counterclock=False, wedgeprops = {'linewidth': 5}, colors = ['#f08b93', '#4286f4'])

	

    #fig1, ax1 = plt.subplots()
    #ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
    #    shadow=True, startangle=90)
    #ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

	
    #plt.xlabel("Cirrhosis",fontsize=15)
    #plt.ylabel( "Percent Chance of Cirrhosis",fontsize=15)
    #plt.ylim(0, 0.05)
	
    # if str(X).strip() == 'age':
        # ax = sns.barplot(patients[X], hist=False, rug=True)
        # plt.title("Age Distribution of Liver Cirrhosis Diasnoses")
        # plt.xlabel("Age (years)",fontsize=15)
        # plt.ylabel( "Percentage (%)",fontsize=15)
        # plt.xlim(0, 100)
        # plt.ylim(0, 0.05)
    
    # if str(X).strip() == 'gender':
        # #patients[X] = patients[X].replace('M', 0, regex=True)
        # #patients[X] = patients[X].replace('F', 1, regex=True)
        # ax = sns.countplot(x='gender', data=patients)
        # plt.title("Gender Distribution of Liver Cirrhosis Diasnoses")
        # plt.xlabel("Gender",fontsize=15)
        # plt.ylabel( "Quantity",fontsize=15)
        # #plt.xlim(0, 100)
        # plt.ylim(0, 1000)

    # if str(X).strip() == 'ethnicity':
        # plt.figure(figsize=(10,10))
        # #patients[X] = patients[X].replace('M', 0, regex=True)
        # #patients[X] = patients[X].replace('F', 1, regex=True)
        # ax = sns.countplot(x='ethnicity', data=patients)
        # #ax.set_xticklabels(ax.get_xticklabels, rotation=70)
        # plt.setp(ax.get_xticklabels(), rotation=90)
        # plt.title("Ethnicity Distribution of Liver Cirrhosis Diasnoses")
        # plt.xlabel("Ethnicity",fontsize=5)
        # plt.ylabel( "Quantity",fontsize=15)
        # #plt.xlim(0, 100)
        # plt.ylim(0, 1000)
        # plt.tight_layout()		
		
    if not os.path.isdir('static'):
        os.mkdir('static')
    else:
       # remove old plot file
       for filename in glob.glob(os.path.join('static', '*.png')):
            os.remove(filename)
    # a unique filename that the browser has not chached
    plotfile = os.path.join('static', str(time.time()) + '.png')
    plt.savefig(plotfile, facecolor = '#fce9eb')
    return plotfile

