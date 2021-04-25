import numpy as np
import pandas as pd
from scipy import stats


def linear_regression(dataset):

    if len(dataset) == 0:
        print("Dataset is empty!")
        return

    if not isinstance(dataset, pd.DataFrame) :
        print("Dataset is not DataFrame, cannot perform Linear Regression.")
        return

    # dataset is a DataFrame object with its y values in the last column, the remaining is X

    for column_name in dataset.columns:
        dataset[column_name] = pd.to_numeric(dataset[column_name], errors="coerce")

    clear_dataset = dataset.dropna(axis=0)

    clear_dataset = clear_dataset.reset_index(drop=True)

    X = clear_dataset.iloc[:, :-1]
    y = clear_dataset[clear_dataset.columns[-1]]

    coefficients = ((np.linalg.inv((X.T).dot(X))).dot(X.T).dot(y))

    y_estimated = X.dot(coefficients)

    error = y - y_estimated

    variance = (((error.T).dot(error))/(len(clear_dataset) - len(X.columns) - 1))*((np.linalg.inv((X.T).dot(X))))

    t_stats = stats.t.ppf(0.95, len(clear_dataset) - 1)

    intervals = []
    for i in range(0, len(coefficients)):
        intervals.append([coefficients[i]-t_stats*variance[i][i], coefficients[i]+t_stats*variance[i][i]])

    print("Total absolute error: ", sum(abs(error)))

    return coefficients, error, intervals

