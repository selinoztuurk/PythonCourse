import numpy as np
import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

data = pd.read_csv("turkey_data.csv", index_col=0)
data.drop(["year"], axis=1, inplace=True)

X = data.iloc[:, :-1]
y = data[data.columns[-1]]

reg = LinearRegression().fit(X, y)

print(reg.coef_)

