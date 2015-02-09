import numpy as np
import pandas as pd

# Import data into pandas dataframe
vote_data_header = ['Party', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 
                    		'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16']

vote_data = pd.read_csv('cong_votes_data.data', header=None)
vote_data.columns = vote_data_header
vote_data = vote_data.replace('y', 1).replace('n', 0)
vote_data.head()

### CHALLENGE #1

# Replace entries with '?' by the column mean
for column in vote_data.columns:
	if column != 'Party':
		column_mean = np.mean(vote_data[column].replace('?',np.nan))
		vote_data[column] = vote_data[column].replace('?', float(column_mean))


### CHALLENGE #2

from sklearn.cross_validation import train_test_split

train_vd_x, test_vd_x, train_vd_y, test_vd_y = train_test_split(vote_data.drop(['Party'], axis=1), 
								vote_data['Party'], test_size=0.30)


### CHALLENGE #3

from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score

# Train KNN classifier for a variety of K choices
knn_accuracy_scores = []

for k in range(1,21):
	knn_classifier = KNeighborsClassifier(n_neighbors=k)
	knn_classifier.fit(train_vd_x, train_vd_y)
	pred_vd_y = knn_classifier.predict(test_vd_x)

	# Test accuracy
    	knn_accuracy_scores.append(accuracy_score(test_vd_y, pred_vd_y))

# Print accuracy scores
print "KNN with with k neighbors\n"

for k, score in enumerate(knn_accuracy_scores):
	print "Accuracy for k = " + str(k+1) + " is: " + str(score)


### CHALLENGE #4

from sklearn.linear_model import LogisticRegression

# Train logistic regression classifier for a variety of C choices (regularization)
logit_accuracy_scores = []

for c in range(-1,4):
	logit_classifier = LogisticRegression(C=(10**c))
	logit_classifier.fit(train_vd_x, train_vd_y)
    	pred_vd_y = logit_classifier.predict(test_vd_x)

    	# Test accuracy
    	logit_accuracy_scores.append(accuracy_score(test_vd_y, pred_vd_y))

# Print accuracy scores
print "Logistic regression with L2 regularization of C\n"

for k, score in enumerate(logit_accuracy_scores):
    	print "Accuracy for C = " + str(10**(k-1)) + " is: " + str(score)


### CHALLENGE #5

import matplotlib.pyplot as plt
import seaborn as sb

# Bar chart of republicans and democrats
colors = ['r','b']
sb.factorplot('Party',data=vote_data)
plt.title('Count of each political party in the votes data')
plt.show()

# Function to predict a single value for all examples
def predict_single_value(value, df):
    	return [str(value)] * len(df)

# If we just predict democrat for everything
pred_vd_y_all_dem = predict_single_value('democrat',test_vd_x)
all_dem_score = accuracy_score(test_vd_y, pred_vd_y_all_dem)
print "If we predict Democrat for everything we get accuracy of " + str(all_dem_score) 

# If we just predict republican for everything
pred_vd_y_all_rep = predict_single_value('republican',test_vd_x)
all_rep_score = accuracy_score(test_vd_y, pred_vd_y_all_rep)
print "If we predict Republican for everything we get accuracy of " + str(all_rep_score) 


### CHALLENGE #6

# Convert non-array scores (not from KNN) into arrays
logit_plotting_scores = [logit_accuracy_scores[2]] * len(knn_accuracy_scores)
dem_plotting_scores = [all_dem_score] * len(knn_accuracy_scores)
rep_plotting_scores = [all_rep_score] * len(knn_accuracy_scores)

# Plot scores
plt.plot(knn_accuracy_scores)
plt.plot(logit_plotting_scores)
plt.plot(dem_plotting_scores)
plt.plot(rep_plotting_scores)
plt.legend(['KNN', 'Logit', 'Just Predict Dem', 'Just Predict Rep'], loc=0)
plt.xlabel('k')
plt.ylabel('Accuracy')
plt.show()


### CHALLENGE #7

from sklearn.learning_curve import learning_curve

# Function which takes a classifier, name, and num obvs, and plots learning curve
def plotLearningFromClassifier(classifier, name, obvs):
   	# Must be more than 20 obvs
    	assert int(obvs) >= 20, "There must be 20 observations"
    
    	# Get the learning curves for 3 different folds
    	train_sizes_input = [(10*(index + 2)) for index in range(int(np.floor(int((obvs - 5) / 10))) - 1)]
    	train_sizes_output, train_scores, test_scores = learning_curve(classifier, vote_data.drop(['Party'], axis=1), vote_data['Party'], train_sizes=train_sizes_input)

    	# Take the mean of the learning curves to get a best guess of actual curve
    	train_cv_err = 1 - np.mean(train_scores,axis=1)                                                                                                                                                           
	test_cv_err = 1 - np.mean(test_scores,axis=1)

	# Plot learning curve
	plt.plot(train_sizes_input, train_cv_err)
	plt.plot(train_sizes_input, test_cv_err)
	plt.xlabel('Number of Training Examples')
	plt.ylabel('Test Error')
	plot_title = 'Learning Curve for ' + str(name) + ' Classifier'
	plt.legend(['Train Error', 'Test Error'], loc=0)
	plt.title(plot_title)
	plt.show()

# Plot learning curve for Logit classifier
plotLearningFromClassifier(logit_classifier, 'Logit', 290)

# Plot learning curve for KNN classifier with k=4 (best)
plotLearningFromClassifier(KNeighborsClassifier(n_neighbors=4), 'KNN', 290)


### CHALLENGE #8

from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier

# Function which takes a classifier and returns the accuracy
def getAccuracyForClassifier(classifier, train_x, test_x, train_y, test_y):
    	classifier.fit(train_x, train_y)
    	pred_y_classifier = classifier.predict(test_x)
    	return accuracy_score(test_y, pred_y_classifier)

# Set up classifiers
gaussian_nb_classifier = GaussianNB()
SVC_classifier = SVC()
tree_classifier = DecisionTreeClassifier()
random_forest_classifier = RandomForestClassifier()

# Get accuracy of classifiers
gaussian_nb_acc = getAccuracyForClassifier(gaussian_nb_classifier, train_vd_x, test_vd_x, train_vd_y, test_vd_y)
SVC_acc = getAccuracyForClassifier(SVC_classifier, train_vd_x, test_vd_x, train_vd_y, test_vd_y)
tree_acc = getAccuracyForClassifier(tree_classifier, train_vd_x, test_vd_x, train_vd_y, test_vd_y)
random_forest_acc = getAccuracyForClassifier(random_forest_classifier, train_vd_x, test_vd_x, train_vd_y, test_vd_y)

# Print accuracy of classifiers
print "The accuracy of the Gaussian Naive Bayes classifier is: " + str(gaussian_nb_acc)
print "The accuracy of the SVM classifier is: " + str(SVC_acc)
print "The accuracy of the Decision Tree classifier is: " + str(tree_acc)
print "The accuracy of the Random Forest classifier is: " + str(random_forest_acc)


### CHALLENGE #9

from sklearn.cross_validation import cross_val_score

# Define function which takes a classifier, num obvs, and returns the cross validation score
def getCVScoreFromClassifier(classifier):
    	scores = cross_val_score(classifier, vote_data.drop(['Party'], axis=1), vote_data['Party'])

    	# Take the mean of the learning curves to get a best guess of actual curve
    	mean_scores = np.mean(scores)    
    	return mean_scores

# Print accuracies
print "The CV score of the Logit classifier is: " + str(getCVScoreFromClassifier(logit_classifier))
print "The CV score of the KNN classifier (k = 4) is: " + str(getCVScoreFromClassifier(KNeighborsClassifier(n_neighbors=4)))
print "The CV score of the Gaussian Naive Bayes classifier is: " + str(getCVScoreFromClassifier(gaussian_nb_classifier))
print "The CV score of the SVM classifier is: " + str(getCVScoreFromClassifier(SVC_classifier))
print "The CV score of the Decision Tree classifier is: " + str(getCVScoreFromClassifier(tree_classifier))
print "The CV score of the Random Forest classifier is: " + str(getCVScoreFromClassifier(random_forest_classifier))


### CHALLENGE #10

# Import data into pandas dataframe
vote_data_header = ['Party', 'V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 
                    'V9', 'V10', 'V11', 'V12', 'V13', 'V14', 'V15', 'V16']

vote_data = pd.read_csv('cong_votes_data.data', header=None)
vote_data.columns = vote_data_header
vote_data = vote_data.replace('y', 1).replace('n', 0)

# Convert ? to mode of the column (in this case, we can use mean >= 0.5)
for column in vote_data.columns:
    	if column != 'Party':
        		column_mean = np.mean(vote_data[column].replace('?',np.nan))
        		vote_data[column] = vote_data[column].replace('?', 1) if column_mean >= 0.5 else vote_data[column].replace('?', 0)

