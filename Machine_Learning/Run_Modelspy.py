# This is just the program was originally planned to be 

# Load libaries
import os
import pandas as pd
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from pydotplus import graph_from_dot_data
from sklearn import preprocessing
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.svm import SVC
from sklearn import svm, metrics
from sklearn.model_selection import GridSearchCV, RandomizedSearchCV
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.model_selection import train_test_split, GridSearchCV, cross_validate, cross_val_score, KFold
from sklearn.model_selection import RepeatedStratifiedKFold
from sklearn.linear_model import ElasticNet
from sklearn.metrics import mean_squared_error
from sklearn.metrics import roc_curve
from sklearn.metrics import roc_auc_score, accuracy_score, f1_score, precision_score, recall_score
from collections import Counter

import warnings

warnings.filterwarnings('ignore')


################################################# CLEANING THE DATA ############################################

### Looking at all of the data

data = pd.DataFrame()

directory_path = "/home/dddenys/jupyterlab_env/ML Models/data_all_years/"
file_list = os.listdir(directory_path)

# Sort the list of files
sorted_files = sorted(file_list)
print("Done sorting")

for filename in file_list:
    file_path = os.path.join(directory_path, filename)

    with open(file_path, 'r') as file:
        print(f"File name: {filename}")
        temp_data = pd.read_csv(file_path, on_bad_lines='skip')
        data = pd.concat([data, temp_data], axis=0)

print("DONE!")

### DATA CLEANING
data.dropna(axis=0, inplace=True) # drop the rows with null values
data.isnull().sum() # return number of missing value for each column

if 'Date' in data:
    data = data.drop(['Date', 'Longitude', 'Latitude'], axis = 1)

data = data[data.TA !=-999]
data = data[data.TA != 3]
data = data[data.TA != 4]

Count=data.Fire.value_counts() #count target feature
print('Proportion:', round(Count[0] / Count[1], 2), ': 1')









# Define the constants
save_location = str("/home/dddenys/jupyterlab_env/ML Models/saved_plots/")  # Save location for the confusion matrexes & other files
###################################### Change Directory ######################################

def trainModel(model, X_train, y_train, X_test, y_test, model_named=None, model_variation=None):
    # train the model
    model.fit(X_train, y_train)
    evaluation_report(model, X_test, y_test, model_named, model_variation)


# Confusion Matrix Method
def confusion_matrix_build(y_test, predicted, model_name):
    NB_cm = confusion_matrix(y_test, predicted)
    group_names = ['TN', 'FP', 'FN', 'TP']
    group_counts = ["{0:0.0f}".format(value) for value in
                    NB_cm.flatten()]
    labels = [f"{v1}\n{v2}" for v1, v2 in
              zip(group_names, group_counts)]
    labels = np.asarray(labels).reshape(2, 2)
    sns.heatmap(NB_cm, annot=labels, fmt='')
    plt.title(model_name)
    plt.ylabel('True label', fontweight='bold')
    plt.xlabel('Predicted label', fontweight='bold')
    plt.savefig(f"{save_location}{model_name}", dpi=300, bbox_inches='tight', transparent=True)


def evaluation_report(clf_model, X_test, y_test, model_name=None, model_variation=None):
    # Test set prediction
    y_prob = clf_model.predict_proba(X_test)
    y_pred = clf_model.predict(X_test)

    print('Classification Report')
    print('=' * 60)
    print(classification_report(y_test, y_pred), "\n")
    print('AUC-ROC')
    print('=' * 60)
    print(roc_auc_score(y_test, y_prob[:, 1]))
    print('=' * 60)
    print('Confusion Matrix')
    confusion_matrix_build(y_test, y_pred, f"{model_name}{model_variation}")



if (__name__ == '__main__'):
    print("I am working !")

    # Getting the X & Y
    X = data.drop(columns=['Fire']).values
    Y = data['Fire'].values

    # Labeling the variables
    scale = StandardScaler()
    X = scale.fit_transform(X)

    # 20% test 80% training data
    X_train, X_test, y_train, y_test, = train_test_split(X, Y, test_size=0.2, random_state=42)

    # 0.25 x 0.8 = 0.2 for validation data
    X_train, X_val, y_train, y_val, = train_test_split(X_train, y_train, test_size=0.25, random_state=16)


    #### Oversamling & undersamling

    from imblearn.pipeline import Pipeline
    from imblearn.over_sampling import SMOTE
    from imblearn.under_sampling import RandomUnderSampler

    oversampling_ratio = 0.1
    # 0.01 means the majority class will be 100 times the size of minority class
    # 0.1 means the majority class will be 10 times the size of minority class

    undersample_ratio = 0.5
    # 0.01 means the majority class will be 100 times the size of minority class
    # 0.1 means the majority class will be 10 times the size of minority class

    counter1 = Counter(y_train)
    print('Before', counter1)

    # define pipeline
    over = SMOTE(sampling_strategy=oversampling_ratio, n_jobs=-1)
    under = RandomUnderSampler(sampling_strategy=undersample_ratio)
    steps = [('o', over), ('u', under)]
    pipeline = Pipeline(steps=steps)
    # transform the dataset
    X_train, y_train = pipeline.fit_resample(X_train, y_train)

    counter = Counter(y_train)
    print('After', counter)

    #Write the models that you are using here
    LR = LogisticRegression(C=0.01, penalty='l2', solver='liblinear', n_jobs=-1)
    mlp = MLPClassifier(hidden_layer_sizes=(8,8,8,8,8,8))
    NB = GaussianNB(var_smoothing=0.0002848035868435802)
    KNN = KNeighborsClassifier(metric='euclidean', n_neighbors=13, weights='uniform', n_jobs=-1)
    RF = RandomForestClassifier(max_features='sqrt', n_estimators=100)
    SVM = SVC(C=10, gamma='scale', kernel='rbf')


    # models = [LR, mlp]
    #LR.fit(X_train, y_train)
    #evaluation_report(NB, X_test, y_test, 'Linear Regression ', ' SMOTE + Random Undersampling')
    #mlp.fit(X_train, y_train)
    #evaluation_report(mlp, X_test, y_test, 'Nural Network ', ' SMOTE + Random Undersampling')

    models = [KNN, SVM]
    KNN.fit(X_train, y_train)
    evaluation_report(KNN, X_test, y_test, 'KNN ', ' SMOTE + Random Undersampling')
    SVM.fit(X_train, y_train)
    evaluation_report(SVM, X_test, y_test, 'Standert Support Vector ', ' SMOTE + Random Undersampling')

    # models = [NB, RF]
    # NB.fit(X_train, y_train)
    # evaluation_report(NB, X_test, y_test, 'Gaussian Naive Bayes ', ' SMOTE + Random Undersampling')
    # RF.fit(X_train, y_train)
    # evaluation_report(mlp, X_test, y_test, 'Random Forrest ', ' SMOTE + Random Undersampling')


