
### BUILD CLASSIFIER TO PREDICT INDIVIDUAL INCOME

import pymysql
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelBinarizer

# Connect to Advark DB
db = pymysql.connect(host="104.236.210.19",user='root',passwd='advark79', database='advark')
cursor = db.cursor()

# Read data from SQL
df = pd.read_sql('SELECT * FROM UCI_data LIMIT 30000', db)

## Preprocessing

# Add binary fields for categorical data
lb = LabelBinarizer()
print df.groupby(['sex']).groups.keys()

lb_bin = lb.fit_transform(df['sex']).T

for num, feature_list in enumerate(lb_bin):
    col_label = lb.classes_[num]
    col_to_append = { col_label : list(feature_list) }
    new_df = pd.DataFrame.from_dict(col_to_append)
    df = pd.concat([df, new_df], axis=1)

## Train classifiers
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier

# Define model features and outcome
X = df[['age', 'education_weight', ' Female']]
y = df['gt_50k']

# Fit models and get probability scores
logit = LogisticRegression()
X_train, X_test, y_train, y_test = cross_validation.train_test_split(X,y,train_size = 0.7)
fitted_logit = logit.fit(X_train,y_train)
logit_score = fitted_logit.predict_proba(X_test)

rf_model = RandomForestClassifier()
fitted_rf = rf_model.fit(X_train,y_train)
rf_score = fitted_rf.predict_proba(X_test)

gb_model = GradientBoostingClassifier(loss='deviance', learning_rate=0.4, n_estimators=500)
fitted_gb = gb_model.fit(X_train,y_train)
gb_score = fitted_gb.predict_proba(X_test)

## Model performance

from sklearn.metrics import roc_auc_score
from sklearn.metrics import roc_curve
from matplotlib import pyplot as plt
import seaborn as sb

# Get ROC curve
fpr_logit, tpr_logit, thresholds_logit = roc_curve(y_test, logit_score[:,1])
fpr_rf, tpr_rf, thresholds_rf = roc_curve(y_test, rf_score[:,1])
fpr_gb, tpr_gb, thresholds_gb = roc_curve(y_test, gb_score[:,1])

# Print AUC scores
print roc_auc_score(y_test, logit_score[:,1])
print roc_auc_score(y_test, rf_score[:,1])
print roc_auc_score(y_test, gb_score[:,1])

# Plot ROC curve
plt.plot(fpr_logit,tpr_logit, color='r')
plt.plot(fpr_rf,tpr_rf, color='g')
plt.plot(fpr_gb,tpr_gb, color='b')
plt.xlim([0,1])
plt.ylim([0,1])
plt.show()

