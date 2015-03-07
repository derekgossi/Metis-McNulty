import pandas as pd
import numpy as np
import pickle
import seaborn as sb
import matplotlib.pyplot as plt


### RELOAD VOTE DATA

# Import data into pandas dataframe
vote_data_header = ['Party', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 
                    		'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16']

vote_data = pd.read_csv('cong_votes_data.data', header=None)
vote_data.columns = vote_data_header
vote_data = vote_data.replace('y', 1).replace('n', 0)
vote_data.head()

# Replace entries with '?' by the column mean
for column in vote_data.columns:
	if column != 'Party':
		column_mean = np.mean(vote_data[column].replace('?',np.nan))
		vote_data[column] = vote_data[column].replace('?', float(column_mean))

# Set Democrat = 1
vote_data['Party'] = vote_data['Party'].replace('democrat', 1).replace('republican', 0)


### TRAIN TEST SPLIT

from sklearn.cross_validation import train_test_split

train_vd_x, test_vd_x, train_vd_y, test_vd_y = train_test_split(vote_data.drop(['Party'], axis=1), 
								vote_data['Party'], test_size=0.75)


### CLASSIFIERS

from sklearn.tree import DecisionTreeClassifier

# Set up classifiers
tree_classifier = DecisionTreeClassifier()
classifiers = [tree_classifier]
classifier_names = ['tree']



