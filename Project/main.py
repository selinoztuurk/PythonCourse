import pandas as pd

pd.options.mode.chained_assignment = None

from sklearn.linear_model import LinearRegression

# Reading the dataset including yearly age distributions in Turkey between 2007-2020
turkey_age_distribution = pd.read_csv("turkey_age_distribution.csv", index_col=0)

# Info for these three years is missing
years_to_predict = [2023, 2022, 2021]
predicted_age_distribution = pd.DataFrame(index=years_to_predict, columns=turkey_age_distribution.columns.values)

# One year's population on a specific age determines the next year's population on that specific age + 1,
# so I determine the yearly population change for each group of people born in the same year.
age_groups_change = pd.DataFrame(index=turkey_age_distribution.index, columns=turkey_age_distribution.columns.values)
temp = pd.DataFrame(index=years_to_predict, columns=turkey_age_distribution.columns.values)
age_groups_change = temp.append(age_groups_change)
age_groups_change.fillna(value=0, inplace=True)

ages = turkey_age_distribution.columns.values.tolist()

for i in range(0, len(ages)):
    if ages[i] == "0" or ages[i] == "75+":  # skipping age 75+, cumulative data
        # skipping age 0, no previous data to forecast
        continue
    else:
        for ind in age_groups_change.index.values:
            if ind == 2007 or ind == 2021 or ind == 2022 or ind == 2023:  # skipping 2021, 2022, 2023, not forecasted yet
                # skipping 2007, no previous data to forecast
                continue
            else:
                age_groups_change[ages[i]][int(ind)] = turkey_age_distribution[ages[i]][int(ind)] - \
                                                       turkey_age_distribution[ages[i - 1]][int(ind) - 1]

# Applying linear regression to determine yearly increase/decrease for each group of people born in the same year
# and using this model to forecast the change in age groups in 2021, 2022 and 2023
for age in age_groups_change.columns.values:
    column = age_groups_change[age]
    X = column.index.values.reshape(-1, 1)
    y = column.values.reshape(-1, 1)

    model = LinearRegression()
    model.fit(X, y)

    X_predict = [[2023], [2022], [2021]]
    y_predict = model.predict(X_predict)

    # Filling the table accordingly
    age_groups_change[age][2023] = y_predict[0]
    age_groups_change[age][2022] = y_predict[1]
    age_groups_change[age][2021] = y_predict[2]

# Allocating a new data frame to determine the number of people for each age in each year
temp = pd.DataFrame(index=years_to_predict, columns=turkey_age_distribution.columns.values)
all_data = temp.append(turkey_age_distribution)

all_ages = all_data.columns.values.tolist()

for i in range(0, len(all_ages)):
    if ages[i] == "0" or ages[i] == "75+":  # Since we cannot make use of previous years' data to determine these ages,
        # we are applying linear regression to the time series of these columns
        # to forecast the population in these ages in 2021, 2022 and 2023
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
    else:  # rest is determined by the previous years' data
        all_data[ages[i]][2023] = all_data[ages[i - 1]][2022] + age_groups_change[ages[i]][2023]
        all_data[ages[i]][2022] = all_data[ages[i - 1]][2021] + age_groups_change[ages[i]][2022]
        all_data[ages[i]][2021] = all_data[ages[i - 1]][2020] + age_groups_change[ages[i]][2021]

all_data.to_csv("predicted_population.csv")  # saving the population data for later use

# the years that each generation was born in between
generation_years = {"silent_gen": range(1928, 1946),
                    "boomers": range(1946, 1965),
                    "gen_x": range(1965, 1981),
                    "gen_y": range(1981, 1997),
                    "gen_z": range(1997, 2013),
                    "gen_alpha": range(2013, 2024)}

generations = ["silent_gen", "boomers", "gen_x", "gen_y", "gen_z", "gen_alpha"]

# allocating a new data frame to find the fractions of each generation among voters
generation_fractions_among_voters = pd.DataFrame(index=all_data.index, columns=generations)

# voters population is a subset of the age distributions
# voting age is 18 in Turkey, so we are only considering the people
# who are older than 18
voters_population = all_data.copy()
voters_population.drop(columns=voters_population.columns[:18], axis=1, inplace=True)

# adding a new column "sum" to this data frame as we will be working with the fractions
voters_population["sum"] = voters_population.sum(axis=1)

# determining how many people belong to each generation in each year
years = voters_population.index.tolist()
ages = voters_population.columns.tolist()

for i in range(0, len(years)):
    generation_sums = [0, 0, 0, 0, 0, 0]    # silent_gen, boomers, gen_x, gen_y, gen_z, gen_alpha
    for j in range(0, len(ages)):
        if ages[j] == "75+":    # certainly belongs to silent generation in each year on our dataset
            generation_sums[0] = generation_sums[0] + voters_population["75+"][years[i]]
        elif ages[j] == "sum":  # skipping, not an age group
            continue
        elif years[i] - int(ages[j]) in generation_years["silent_gen"]:
            generation_sums[0] = generation_sums[0] + voters_population[ages[j]][years[i]]
        elif years[i] - int(ages[j]) in generation_years["boomers"]:
            generation_sums[1] = generation_sums[1] + voters_population[ages[j]][years[i]]
        elif years[i] - int(ages[j]) in generation_years["gen_x"]:
            generation_sums[2] = generation_sums[2] + voters_population[ages[j]][years[i]]
        elif years[i] - int(ages[j]) in generation_years["gen_y"]:
            generation_sums[3] = generation_sums[3] + voters_population[ages[j]][years[i]]
        elif years[i] - int(ages[j]) in generation_years["gen_z"]:
            generation_sums[4] = generation_sums[4] + voters_population[ages[j]][years[i]]
        elif years[i] - int(ages[j]) in generation_years["gen_alpha"]:
            generation_sums[5] = generation_sums[5] + voters_population[ages[j]][years[i]]
    generation_fractions = [generation_sums[0] / voters_population["sum"][years[i]],
                            generation_sums[1] / voters_population["sum"][years[i]],
                            generation_sums[2] / voters_population["sum"][years[i]],
                            generation_sums[3] / voters_population["sum"][years[i]],
                            generation_sums[4] / voters_population["sum"][years[i]],
                            generation_sums[5] / voters_population["sum"][years[i]]]
    generation_fractions_among_voters.loc[years[i]] = generation_fractions

generation_fractions_among_voters.to_csv("generation_fractions_among_voters.csv")  # saving the data for later use


# Using third party API to retrieve data on GDP and unemployment rates in Turkey
import quandl

quandl.ApiConfig.api_key = '_aX1xHskAYEELbjqxixh'
needed_columns = ["year", "value"]

# GDP per capita ($) - Turkey
gdp = quandl.get_table('WB/DATA', series_id='NY.GDP.PCAP.CD', country_code='TUR')
gdp = gdp[needed_columns]
gdp.columns = gdp.columns.str.replace("value", "gdp_per_capita")
gdp = gdp.set_index("year")

# GDP predictor
# I am using only the last 5 years' data since this is the only way to preserve the decreasing trend.
# When I use all years' data to forecast GDP for the following years, I received very absurd GDP's
# such as 2 billion $ per capita!? :)
X_gdp = gdp.head(6)["gdp_per_capita"].values.reshape(-1, 1)
X_gdp = X_gdp[-5:]
y_gdp = gdp.head(5)["gdp_per_capita"].values.reshape(-1, 1)

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

# Unemployment rate predictor
# I am using only the last 10 years' data since they are more relevant
X_un = unemployment.head(11)["unemployment_rate"].values.reshape(-1, 1)
X_un = X_un[-10:]
y_un = unemployment.head(10)["unemployment_rate"].values.reshape(-1, 1)

model = LinearRegression()
model.fit(X_un, y_un)

un_prediction_2020 = model.predict([[unemployment["unemployment_rate"][2019]]])
un_prediction_2021 = model.predict(un_prediction_2020)
un_prediction_2022 = model.predict(un_prediction_2021)
un_prediction_2023 = model.predict(un_prediction_2022)

# joining the unemployment and gdp tables with the generation fractions dataset

aggregate_data = generation_fractions_among_voters.join(other=gdp, how="left")

aggregate_data["gdp_per_capita"][2020] = gdp_prediction_2020
aggregate_data["gdp_per_capita"][2021] = gdp_prediction_2021
aggregate_data["gdp_per_capita"][2022] = gdp_prediction_2022
aggregate_data["gdp_per_capita"][2023] = gdp_prediction_2023

aggregate_data = aggregate_data.join(other=unemployment, how="left")

aggregate_data["unemployment_rate"][2020] = un_prediction_2020
aggregate_data["unemployment_rate"][2021] = un_prediction_2021
aggregate_data["unemployment_rate"][2022] = un_prediction_2022
aggregate_data["unemployment_rate"][2023] = un_prediction_2023

# reading the previous elections' data
election_results = pd.read_csv("election_results.csv", index_col="election_year")

# joining the election results with the aggregate dataset
# this join operation allows concatenation on matching years only
training_data = election_results.join(other=aggregate_data, how="inner")

X = training_data[["attendance_rate", "month", "boomers", "gen_z", "gdp_per_capita", "unemployment_rate"]]
y = training_data["akp_favor"]

model = LinearRegression()
model.fit(X, y)

X_predict = [
    [0.75, 3, aggregate_data["boomers"][2023], aggregate_data["gen_z"][2023], aggregate_data["gdp_per_capita"][2023],
     aggregate_data["unemployment_rate"][2023]]]

X_predict = [
    [0.75, 6, aggregate_data["boomers"][2023], aggregate_data["gen_z"][2023], aggregate_data["gdp_per_capita"][2023],
     aggregate_data["unemployment_rate"][2023]]]

X_predict = [
    [0.75, 3, aggregate_data["boomers"][2022], aggregate_data["gen_z"][2022], aggregate_data["gdp_per_capita"][2022],
     aggregate_data["unemployment_rate"][2022]]]

X_predict = [
    [0.75, 6, aggregate_data["boomers"][2022], aggregate_data["gen_z"][2022], aggregate_data["gdp_per_capita"][2022],
     aggregate_data["unemployment_rate"][2022]]]

X_predict = [
    [0.75, 3, aggregate_data["boomers"][2021], aggregate_data["gen_z"][2021], aggregate_data["gdp_per_capita"][2021],
     aggregate_data["unemployment_rate"][2021]]]


X_predict = [
    [0.75, 6, aggregate_data["boomers"][2021], aggregate_data["gen_z"][2021], aggregate_data["gdp_per_capita"][2021],
     aggregate_data["unemployment_rate"][2021]]]
"""
"""

y_predict = model.predict(X_predict)

y_predict_checking_errors = model.predict(X)

error = training_data["akp_favor"] - y_predict_checking_errors
error_sq = error*error
error_sum_of_sq = error_sq.sum(axis=0)

print("done")
