import pandas as pd
from sklearn.linear_model import LinearRegression

turkey_age_distribution = pd.read_csv("turkey_age_distribution.csv", index_col=0)
years_to_predict = [2023, 2022, 2021]

predicted_age_distribution = pd.DataFrame(index=years_to_predict, columns=turkey_age_distribution.columns.values)

age_groups_change = pd.DataFrame(index=turkey_age_distribution.index, columns=turkey_age_distribution.columns.values)

temp = pd.DataFrame(index=years_to_predict, columns=turkey_age_distribution.columns.values)
age_groups_change = temp.append(age_groups_change)
age_groups_change.fillna(value=0,inplace=True)

ages = turkey_age_distribution.columns.values.tolist()

for i in range(0, len(ages)):
    if ages[i]=="0" or ages[i]=="75+":
        continue
    else:
        for ind in age_groups_change.index.values:
            if ind==2007 or ind==2021 or ind==2022 or ind==2023:
                continue
            else:
                age_groups_change[ages[i]][int(ind)] = turkey_age_distribution[ages[i]][int(ind)] - turkey_age_distribution[ages[i-1]][int(ind)-1]

for age in age_groups_change.columns.values:

    column = age_groups_change[age]
    X = column.index.values.reshape(-1, 1)
    y = column.values.reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, y)

    X_predict = [[2023], [2022], [2021]]
    y_predict = model.predict(X_predict)
    age_groups_change[age][2023] = y_predict[0]
    age_groups_change[age][2022] = y_predict[1]
    age_groups_change[age][2021] = y_predict[2]

temp = pd.DataFrame(index=years_to_predict, columns=turkey_age_distribution.columns.values)
all_data = temp.append(turkey_age_distribution)

all_ages = all_data.columns.values.tolist()

for i in range(0, len(all_ages)):
    if ages[i]=="0" or ages[i]=="75+":
        column = turkey_age_distribution[ages[i]]
        X = column.index.values.reshape(-1, 1)
        y = column.values.reshape(-1, 1)

        model = LinearRegression()
        model.fit(X, y)

        X_predict = [[2023], [2022], [2021]]
        y_predict = model.predict(X_predict)

        all_data[ages[i]][2023] = int(y_predict[0][0])
        all_data[ages[i]][2022] = int(y_predict[1][0])
        all_data[ages[i]][2021] = int(y_predict[2][0])
    else:
        all_data[ages[i]][2023] = all_data[ages[i-1]][2022] + age_groups_change[ages[i]][2023]
        all_data[ages[i]][2022] = all_data[ages[i-1]][2021] + age_groups_change[ages[i]][2022]
        all_data[ages[i]][2021] = all_data[ages[i-1]][2020] + age_groups_change[ages[i]][2021]

all_data.to_csv("predicted_population.csv")

print("done")