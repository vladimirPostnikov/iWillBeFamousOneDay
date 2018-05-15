import pandas as pd
import numpy as np
from sklearn.preprocessing import Imputer
from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier
import math
import matplotlib as plt
import csv

def kNN(column, data, neighs):
    
    #get training data
    X_train = data.drop(column,1)
    y_train = data[column].astype(int)
    
    #create, train model
    classifier = KNeighborsClassifier(n_neighbors=neighs)
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
	all_data[['alcoholabuse', 'alcoholdependence', 'alcoholicliverdisease']] = \
		all_data[['alcoholabuse', 'alcoholdependence', 'alcoholicliverdisease']].replace( \
		np.nan, 0, regex=True)
	all_data[['alcoholabuse', 'alcoholdependence', 'alcoholicliverdisease']] = \
		all_data[['alcoholabuse', 'alcoholdependence', 'alcoholicliverdisease']].replace( \
		'Present', 1, regex=True)
	
	#replace unique races in df with ints
	#races = all_data.ethnicity.unique()
	#for index, race in enumerate(races):
	#	all_data['ethnicity'] = all_data['ethnicity'].replace(race, index)
	
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
	
	
	classifier = kNN('cirrhosis', all_data, 50)
	
train_model()