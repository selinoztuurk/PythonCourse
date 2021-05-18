import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Reading the data
data = pd.read_csv("cses4_cut.csv")
data = data.dropna(axis=0)  # has no effect since there are no NaN values on this dataset
data = data.drop(data.columns[0], axis=1)  # dropping the first column, since there are some missing indices
# print(data)

# Replacing column codes with variable names
f = open("csesCodebook.txt", "r")
codes_dict = {}
for line in f.readlines():
    if "D20" in line:
        l = line.split("\n")
        cols = l[0].split("    ")
        codes_dict[cols[1]] = cols[-1].lstrip()
f.close()

data = data.rename(columns=codes_dict)
# print(data)

nan_values_1 = [97, 98, 99]
nan_values_2 = [7, 8, 9]
nan_values_3 = [996, 997, 998, 999]

# print(data.groupby(["GENDER"]).count())  # saw that there are no NaN answers, moving on

# print(data.groupby(["EDUCATION"]).count())  # found some NaN answers, removing those rows (40 rows to removed)
data.drop(data[(data["EDUCATION"].isin(nan_values_1))].index, inplace=True)

# print(data.groupby(["MARITAL STATUS"]).count())  # found some NaN answers, removing those rows (762 rows removed)
data.drop(data[data["MARITAL STATUS"].isin(nan_values_2)].index, inplace=True)

# print(data.groupby(["UNION MEMBERSHIP OF RESPONDENT"]).count())
# found some NaN answers, removing those rows (1168 rows removed)
data.drop(data[data["UNION MEMBERSHIP OF RESPONDENT"].isin(nan_values_2)].index, inplace=True)

# print(data.groupby(["UNION MEMBERSHIP OF OTHERS IN HOUSEHOLD"]).count())
# found some NaN answers, removing those rows (1149 rows removed)
data.drop(data[data["UNION MEMBERSHIP OF OTHERS IN HOUSEHOLD"].isin(nan_values_2)].index, inplace=True)

# print(data.groupby(["BUSINESS OR EMPLOYERS' ASSOCIATION MEMBERSHIP"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("BUSINESS OR EMPLOYERS' ASSOCIATION MEMBERSHIP", axis=1)

# print(data.groupby(["FARMERS' ASSOCIATION MEMBERSHIP"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("FARMERS' ASSOCIATION MEMBERSHIP", axis=1)

# print(data.groupby(["PROFESSIONAL ASSOCIATION MEMBERSHIP"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("PROFESSIONAL ASSOCIATION MEMBERSHIP", axis=1)

# print(data.groupby(["CURRENT EMPLOYMENT STATUS"]).count())
# found some NaN answers, removing those rows (39 rows removed)
data.drop(data[data["CURRENT EMPLOYMENT STATUS"].isin(nan_values_1)].index, inplace=True)

# print(data.groupby(["MAIN OCCUPATION"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("MAIN OCCUPATION", axis=1)

# print(data.groupby(["SOCIO ECONOMIC STATUS"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("SOCIO ECONOMIC STATUS", axis=1)

# print(data.groupby(["EMPLOYMENT TYPE - PUBLIC OR PRIVATE"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("EMPLOYMENT TYPE - PUBLIC OR PRIVATE", axis=1)

# print(data.groupby(["INDUSTRIAL SECTOR"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("INDUSTRIAL SECTOR", axis=1)

# print(data.groupby(["SPOUSE: CURRENT EMPLOYMENT STATUS"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("SPOUSE: CURRENT EMPLOYMENT STATUS", axis=1)

# print(data.groupby(["SPOUSE: OCCUPATION"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("SPOUSE: OCCUPATION", axis=1)

# print(data.groupby(["SPOUSE: SOCIO ECONOMIC STATUS"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("SPOUSE: SOCIO ECONOMIC STATUS", axis=1)

# print(data.groupby(["SPOUSE: EMPLOYMENT TYPE - PUBLIC OR PRIVATE"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("SPOUSE: EMPLOYMENT TYPE - PUBLIC OR PRIVATE", axis=1)

# print(data.groupby(["SPOUSE: INDUSTRIAL SECTOR"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("SPOUSE: INDUSTRIAL SECTOR", axis=1)

# print(data.groupby(["HOUSEHOLD INCOME"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("HOUSEHOLD INCOME", axis=1)

# print(data.groupby(["NUMBER IN HOUSEHOLD IN TOTAL"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("NUMBER IN HOUSEHOLD IN TOTAL", axis=1)

# print(data.groupby(["NUMBER OF CHILDREN IN HOUSEHOLD UNDER AGE 18"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("NUMBER OF CHILDREN IN HOUSEHOLD UNDER AGE 18", axis=1)

# print(data.groupby(["NUMBER IN HOUSEHOLD UNDER AGE 6"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("NUMBER IN HOUSEHOLD UNDER AGE 6", axis=1)

# print(data.groupby(["RELIGIOUS SERVICES ATTENDANCE"]).count())
# found some NaN answers, removing those rows (204 rows removed)
data.drop(data[data["RELIGIOUS SERVICES ATTENDANCE"].isin(nan_values_2)].index, inplace=True)

# print(data.groupby(["RELIGIOSITY"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("RELIGIOSITY", axis=1)

# print(data.groupby(["RELIGIOUS DENOMINATION"]).count())
# dropping this column because the definitions of the codes in the website are inconsistent
# analysis won't be meaningful and add extra computational work, let's get rid of this column entirely
data = data.drop("RELIGIOUS DENOMINATION", axis=1)

# print(data.groupby(["LANGUAGE USUALLY SPOKEN AT HOME"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("LANGUAGE USUALLY SPOKEN AT HOME", axis=1)

# print(data.groupby(["REGION OF RESIDENCE"]).count())
# dropping this column because there are no definitions of the codes in the website
# analysis won't be meaningful and add extra computational work, let's get rid of this column entirely
data = data.drop("REGION OF RESIDENCE", axis=1)

# print(data.groupby(["RACE"]).count())
# print(data.groupby(["ETHNICITY"]).count())
# removing NaN rows on these columns will cause a lot of information loss, thus dropping these columns completely
data = data.drop("RACE", axis=1)
data = data.drop("ETHNICITY", axis=1)

# print(data.groupby(["RURAL OR URBAN RESIDENCE"]).count())
# removing NaN rows on this column will cause a lot of information loss, thus dropping this column completely
data = data.drop("RURAL OR URBAN RESIDENCE", axis=1)

data = data.reset_index(drop=True)

# Numerating the last column
data['voted'] = data['voted'].replace({True: 1, False: 0})
data.to_csv("with_column_names.csv")

columns_to_be_ohed = list(data.columns)
columns_to_be_ohed.remove("RELIGIOUS SERVICES ATTENDANCE")
columns_to_be_ohed.remove("EDUCATION")
columns_to_be_ohed.remove("age")
columns_to_be_ohed.remove("voted")

for col_name in columns_to_be_ohed:
    y = pd.get_dummies(data[col_name], prefix=col_name)
    data = data.drop(col_name, axis=1)
    data = data.join(y)

# Determining the feature matrix (X) and target (y)
X = data.drop("voted", axis=1)
y = data["voted"]

# Splitting data into train & test subsets
from sklearn.model_selection import train_test_split
Xtrain, Xtest, ytrain, ytest = train_test_split(X, y, random_state=1)

# Trying the GaussianNB model
from sklearn.naive_bayes import GaussianNB
model = GaussianNB()
model.fit(Xtrain, ytrain)
y_model = model.predict(Xtest)

# Accuracy of GaussianNB
from sklearn.metrics import accuracy_score
print("GaussianNB accuracy:", accuracy_score(ytest, y_model))  # returns 0.7919

# Cross Validation for GaussianNB
from sklearn.model_selection import cross_val_score
print("Cross Validation for GaussianNB:", cross_val_score(model, X, y, cv=5))
print("Mean:", cross_val_score(model, X, y, cv=5).mean()) # returns 0.7725
print()

# Trying the SGDClassifier model
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
clf = make_pipeline(StandardScaler(), SGDClassifier(random_state=1))
clf.fit(Xtrain, ytrain)
print("SGDClassifier accuracy:", clf.score(Xtest, ytest))  # returns 0.8399
print()

# Trying the LinearSVC model
from sklearn.svm import LinearSVC
clf = make_pipeline(StandardScaler(), LinearSVC(random_state=1, max_iter=10000))
clf.fit(Xtrain, ytrain)
print("LinearSVC accuracy:", clf.score(Xtest, ytest))  # returns 0.8469
print()

# Trying the DecisionTreeClassifier model
from sklearn import tree
from sklearn.model_selection import cross_val_score
treeclassifier = tree.DecisionTreeClassifier(max_depth=4, random_state=1)
treeclassifier = treeclassifier.fit(Xtrain, ytrain)
print("Cross Validation for DecisionTreeClassifier: ", cross_val_score(treeclassifier, Xtest, ytest, cv=5))
print("Mean:", cross_val_score(treeclassifier, Xtest, ytest, cv=5).mean()) # returns 0.8605
print()
text_representation = tree.export_text(decision_tree=treeclassifier, feature_names=list(X.columns))
print(text_representation)

