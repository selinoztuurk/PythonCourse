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

generation_years = {"silent_gen": range(1928, 1946),
                    "boomers": range(1946, 1965),
                    "gen_x": range(1965, 1981),
                    "gen_y": range(1981, 1997),
                    "gen_z": range(1997, 2013),
                    "gen_alpha": range(2013, 2024)}

generations = ["silent_gen", "boomers", "gen_x", "gen_y", "gen_z", "gen_alpha"]

generation_fractions_among_voters = pd.DataFrame(index=all_data.index, columns=generations)

voters_population = all_data.copy()
voters_population.drop(columns=voters_population.columns[:18], axis=1, inplace=True)
voters_population["sum"] = voters_population.sum(axis=1)

years = voters_population.index.tolist()
ages = voters_population.columns.tolist()

for i in range(0, len(years)):
    generation_sums = [0, 0, 0, 0, 0, 0]
    for j in range(0, len(ages)):
        if ages[j]=="75+":
            generation_sums[0] = generation_sums[0] + voters_population["75+"][years[i]]
        elif ages[j]=="sum":
            continue
        elif years[i]-int(ages[j]) in generation_years["silent_gen"]:
            generation_sums[0] = generation_sums[0] + voters_population[ages[j]][years[i]]
        elif years[i]-int(ages[j]) in generation_years["boomers"]:
            generation_sums[1] = generation_sums[1] + voters_population[ages[j]][years[i]]
        elif years[i]-int(ages[j]) in generation_years["gen_x"]:
            generation_sums[2] = generation_sums[2] + voters_population[ages[j]][years[i]]
        elif years[i]-int(ages[j]) in generation_years["gen_y"]:
            generation_sums[3] = generation_sums[3] + voters_population[ages[j]][years[i]]
        elif years[i]-int(ages[j]) in generation_years["gen_z"]:
            generation_sums[4] = generation_sums[4] + voters_population[ages[j]][years[i]]
        elif years[i]-int(ages[j]) in generation_years["gen_alpha"]:
            generation_sums[5] = generation_sums[5] + voters_population[ages[j]][years[i]]
    generation_fractions = [generation_sums[0]/voters_population["sum"][years[i]],
                            generation_sums[1]/voters_population["sum"][years[i]],
                            generation_sums[2]/voters_population["sum"][years[i]],
                            generation_sums[3]/voters_population["sum"][years[i]],
                            generation_sums[4]/voters_population["sum"][years[i]],
                            generation_sums[5]/voters_population["sum"][years[i]]]
    generation_fractions_among_voters.loc[years[i]] = generation_fractions

generation_fractions_among_voters.to_csv("generation_fractions_among_voters.csv")

import quandl

quandl.ApiConfig.api_key = '_aX1xHskAYEELbjqxixh'
needed_columns = ["year", "value"]

# GDP per capita ($) - Turkey
gdp = quandl.get_table('WB/DATA', series_id='NY.GDP.PCAP.CD', country_code='TUR')
gdp = gdp[needed_columns]
gdp.columns = gdp.columns.str.replace("value", "gdp_per_capita")
gdp = gdp.set_index("year")

# gdp predictor
X_gdp = gdp.head(6)["gdp_per_capita"].values.reshape(-1,1)
X_gdp = X_gdp[-5:]
y_gdp = gdp.head(5)["gdp_per_capita"].values.reshape(-1,1)

model = LinearRegression()
model.fit(X_gdp, y_gdp)

gdp_prediction_2020 = model.predict([[gdp["gdp_per_capita"][2019]]])
gdp_prediction_2021 = model.predict(gdp_prediction_2020)
gdp_prediction_2022 = model.predict(gdp_prediction_2021)
gdp_prediction_2023 = model.predict(gdp_prediction_2022)

# Unemployment Rate (% of total labor force) - Turkey
unemployment = quandl.get_table('WB/DATA', series_id='SL.UEM.TOTL.NE.ZS', country_code='TUR')
unemployment = unemployment[needed_columns]
unemployment.columns = unemployment.columns.str.replace("value", "unemployment_rate")
unemployment = unemployment.set_index("year")

# unemployment predictor
X_un = unemployment.head(11)["unemployment_rate"].values.reshape(-1,1)
X_un = X_un[-10:]
y_un = unemployment.head(10)["unemployment_rate"].values.reshape(-1,1)

model = LinearRegression()
model.fit(X_un, y_un)

un_prediction_2020 = model.predict([[unemployment["unemployment_rate"][2019]]])
un_prediction_2021 = model.predict(un_prediction_2020)
un_prediction_2022 = model.predict(un_prediction_2021)
un_prediction_2023 = model.predict(un_prediction_2022)

aggregate_data = generation_fractions_among_voters.join(other=gdp, how="left")

aggregate_data["gdp_per_capita"][2020] = gdp_prediction_2020
aggregate_data["gdp_per_capita"][2021] = gdp_prediction_2021
aggregate_data["gdp_per_capita"][2022] = gdp_prediction_2022
aggregate_data["gdp_per_capita"][2023] = gdp_prediction_2023

aggregate_data= aggregate_data.join(other=unemployment, how="left")

aggregate_data["unemployment_rate"][2020] = un_prediction_2020
aggregate_data["unemployment_rate"][2021] = un_prediction_2021
aggregate_data["unemployment_rate"][2022] = un_prediction_2022
aggregate_data["unemployment_rate"][2023] = un_prediction_2023

#X = aggregate_data.iloc[-13:].index.values.reshape(-1, 1)
#y = aggregate_data.iloc[-13:]["gdp_per_capita"].values.reshape(-1, 1)

#model = LinearRegression()
#model.fit(X, y)

#X_predict = [[2023], [2022], [2021], [2020]]
#y_predict = model.predict(X_predict)
#aggregate_data["gdp_per_capita"][2023] = y_predict[0]
#aggregate_data["gdp_per_capita"][2022] = y_predict[1]
#aggregate_data["gdp_per_capita"][2021] = y_predict[2]
#aggregate_data["gdp_per_capita"][2020] = y_predict[3]

election_results = pd.read_csv("election_results.csv", index_col="election_year")

training_data = election_results.join(other=aggregate_data, how="inner")

X = training_data[["attendance_rate", "month", "boomers", "gen_z", "gdp_per_capita", "unemployment_rate"]]
y = training_data["akp_favor"]

model = LinearRegression()
model.fit(X, y)

X_predict = [[0.85, 3, aggregate_data["boomers"][2023], aggregate_data["gen_z"][2023], aggregate_data["gdp_per_capita"][2023], aggregate_data["unemployment_rate"][2023]]]

#X_predict = [[0.85, 3, aggregate_data["boomers"][2021], aggregate_data["gen_z"][2021]]]

y_predict = model.predict(X_predict)

print("done")