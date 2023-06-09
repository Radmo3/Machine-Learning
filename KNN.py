# -*- coding: utf-8 -*-
"""ALY6020_MOD1.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XQZdlCFn6ZIbaf0PSfgLKohYQiSTjc6I
"""

# Commented out IPython magic to ensure Python compatibility.
#Loading Libraries 
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sb
import plotly.express as pe
import warnings
import seaborn as sb
# %matplotlib inline
from sklearn import metrics
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

from google.colab import files
uploaded = files.upload()

import io 
df = pd.read_csv(io.BytesIO(uploaded['adult-all.csv']))
df

#Add the new columns names
column = ['Age','Workclass','fnlgt','education','education-num','marital-status','occupation','relationship','race','sex','capital-gain'
          ,'capital-loss','hours-per-week','native-country','salary']
df= pd.read_csv(io.BytesIO(uploaded['adult-all.csv']), names= column)
df

# Create bar plots of job and education level by salary
plt.figure(figsize=(12, 6))
sns.countplot(x="Workclass", hue="salary", data=df)
plt.xticks(rotation=45)
plt.title("Distribution of Job Types by Salary")
plt.show()

plt.figure(figsize=(12, 6))
sns.countplot(x="education", hue="salary", data=df)
plt.xticks(rotation=45)
plt.title("Distribution of Education Levels by Salary")
plt.show()

# Create box plots of age, hours worked per week, and capital gain by salary
plt.figure(figsize=(12, 6))
sns.boxplot(x="salary", y="Age", data=df)
plt.title("Distribution of Age by Salary")
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x="salary", y="hours-per-week", data=df)
plt.title("Distribution of Hours Worked Per Week by Salary")
plt.show()

plt.figure(figsize=(12, 6))
sns.boxplot(x="salary", y="capital-gain", data=df)
plt.title("Distribution of Capital Gain by Salary")
plt.show()

#renaming the columns
df = df.rename(columns={
    'Age': 'Age',
    'Workclass': 'Employment',
    'education': 'Education',
    'education-num': 'Education_Num',
    'marital-status': 'Marital_Status',
    'occupation': 'Occupation',
    'relationship': 'Relationship',
    'race': 'Race',
    'sex': 'Sex',
    'capital-gain': 'Capital_Gain',
    'capital-loss': 'Capital_Loss',
    'hours-per-week': 'Hours_Per_Week',
    'native-country': 'Native_Country',
    'salary': 'Salary'
})
df

df.isnull().sum()

# Convert Employment to binary variable
df['Employment'] = df['Employment'].apply(lambda x: 'Unemployed' if x in ['Without-pay', 'Never-worked'] else 'Employed')

# Convert Education to numerical variable
education_dict = {
    'Preschool': 0,
    '1st-4th': 1,
    '5th-6th': 2,
    '7th-8th': 3,
    '9th': 4,
    '10th': 5,
    '11th': 6,
    '12th': 7,
    'HS-grad': 8,
    'Some-college': 9,
    'Assoc-voc': 10,
    'Assoc-acdm': 11,
    'Bachelors': 12,
    'Masters': 13,
    'Prof-school': 14,
    'Doctorate': 15
}
df['Education_Num'] = df['Education'].map(education_dict)

# Convert categorical variables to numerical variables
df = pd.get_dummies(df, columns=['Employment', 'Marital_Status', 'Occupation', 'Relationship', 'Race', 'Sex', 'Native_Country'])
df

# Impute missing values with column mean
df.fillna(df.mean(), inplace=True)

# Encode target variable
from sklearn.preprocessing import LabelEncoder

label_encoder = LabelEncoder()
df['Salary'] = label_encoder.fit_transform(df['Salary'])

# Split data into train and test sets
X = df.drop('Salary', axis=1)
y = df['Salary']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# define independent variables for models
# define the independent variables for the three models
X1 = df[['Age', 'Capital_Gain', 'Capital_Loss']]
X2 = df[['Education_Num', 'Hours_Per_Week', 'Capital_Gain']]
X3 = df[['Age', 'Education_Num', 'Hours_Per_Week']]
# define the dependent variable
y = df['Salary']

# repeat the process 10 times with different random splits of the data
num_trials = 10
results = []
for i in range(num_trials):
    # split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X1, y, test_size=0.3, random_state=i)

# fit the KNN model on the training data
model1 = KNeighborsClassifier(n_neighbors=5)
model1.fit(X_train, y_train)

# evaluating the model on the testing data and store the accuracy
y_pred = model1.predict(X_test)
accuracy1 = accuracy_score(y_test, y_pred)

# repeating the same process for the second model
X_train, X_test, y_train, y_test = train_test_split(X2, y, test_size=0.3, random_state=i)
model2 = KNeighborsClassifier(n_neighbors=5)
model2.fit(X_train, y_train)
y_pred = model2.predict(X_test)
accuracy2 = accuracy_score(y_test, y_pred)

# repeating the same process for the third model
X_train, X_test, y_train, y_test = train_test_split(X3, y, test_size=0.3, random_state=i)
model3 = KNeighborsClassifier(n_neighbors=5)
model3.fit(X_train, y_train)
y_pred = model3.predict(X_test)
accuracy3 = accuracy_score(y_test, y_pred)

# store the results for this trial
results.append((acc1, acc2, acc3))

# compute the average accuracy for each model
accuracy1_avg = sum([r[0] for r in results]) / num_trials
accuracy2_avg = sum([r[1] for r in results]) / num_trials
accuracy3_avg = sum([r[2] for r in results]) / num_trials

# print the results
print('Model 1 (Age, Capital-Gain, Capital-Loss) accuracy:', acc1_avg)
print('Model 2 (Education-Num, Hours-Per-Week, Capital-Gain) accuracy:', acc2_avg)
print('Model 3 (Age, Education-Num, Hours-Per-Week) accuracy:', acc3_avg)

import matplotlib.pyplot as plt
 
# create a list of accuracy scores for each model
accuracy_scores = [acc1, acc2, acc3]
 
# create a list of independent variables used in each model
independent_vars = ['Model 1', 'Model 2', 'Model 3']
 
# create a bar chart showing the accuracy scores of each model
plt.bar(independent_vars, accuracy_scores, color=['blue', 'green', 'orange'])
plt.title('Comparison of KNN Models')
plt.xlabel('Independent Variables')
plt.ylabel('Accuracy Score')
plt.show()

