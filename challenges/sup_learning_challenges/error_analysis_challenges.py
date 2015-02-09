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

from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Set up classifiers
logit_classifier = LogisticRegression()
knn_classifier = KNeighborsClassifier()
gaussian_nb_classifier = GaussianNB()
SVC_classifier = SVC( probability=True )
tree_classifier = DecisionTreeClassifier()
random_forest_classifier = RandomForestClassifier()

classifiers = [ logit_classifier, knn_classifier, gaussian_nb_classifier, SVC_classifier, 
		tree_classifier, random_forest_classifier ]

classifier_names = [ 'logit', 'knn', 'nb', 'svm', 'tree', 'forest' ]


### CHALLENGE #1 + 2

from sklearn import metrics

# Get accuracy scores for a classifier
def getAccuracyScoresForClassifier(classifier, train_x, test_x, train_y, test_y):
    	classifier.fit(train_x, train_y)
    	pred_y_classifier = classifier.predict(test_x)
    	y_score = classifier.predict_proba(test_x)

    	# Scores
    	accuracy_score = metrics.accuracy_score(test_y, pred_y_classifier)
    	precision_score = metrics.precision_score(test_y, pred_y_classifier)
    	recall_score = metrics.recall_score(test_y, pred_y_classifier)
    	f1_score = metrics.f1_score(test_y, pred_y_classifier)
    	auc = metrics.roc_auc_score(test_y, pred_y_classifier)
    	roc_curve = metrics.roc_curve(test_y, y_score[ :, 1 ])

    	return ( accuracy_score, precision_score, recall_score,
    		f1_score, auc, roc_curve )



# Get accuracy scores for our classifiers
accuracy_scores = {}

for classifier, classifier_name in zip(classifiers, classifier_names):
	accuracy_score, precision_score, recall_score, f1_score, auc, roc_curve = getAccuracyScoresForClassifier(classifier,
												train_vd_x, test_vd_x, train_vd_y, test_vd_y)
	accuracy_scores[classifier_name] = { "accuracy" : accuracy_score, "precision" : precision_score, 
						"recall" : recall_score, "f1_score" : f1_score, "auc" : auc,
						"roc_curve" : roc_curve }

# Plot ROC curves
for name in classifier_names:
	plt.plot( accuracy_scores[name]['roc_curve'][0], accuracy_scores[name]['roc_curve'][1] )

plt.xlim( [0,1] )
plt.ylim( [0,1] )
plt.title('ROC curves for classifiers')
plt.legend(classifier_names)
plt.show()


