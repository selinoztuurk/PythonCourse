import pandas as pd
import quandl

from Homework2 import linearRegression as lr

quandl.ApiConfig.api_key = '_aX1xHskAYEELbjqxixh'
needed_columns = ["year", "value"]

# Urban population (% of total population) - Turkey
data_1 = quandl.get_table('WB/DATA', series_id='SP.URB.TOTL.IN.ZS', country_code='TUR')
data_1 = data_1[needed_columns]
data_1.columns = data_1.columns.str.replace("value", "urban_population_percent")

# Fertility rate (births per woman), total (years) - Turkey
data_2 = quandl.get_table('WB/DATA', series_id='SP.DYN.TFRT.IN', country_code='TUR')
data_2 = data_2[needed_columns]
data_2.columns = data_2.columns.str.replace("value", "fertility_rate")

# Population ages 0-14 (% of total population) - Turkey
data_3 = quandl.get_table('WB/DATA', series_id='SP.POP.0014.TO.ZS', country_code='TUR')
data_3 = data_3[needed_columns]
data_3.columns = data_3.columns.str.replace("value", "child_population")

# Life expectancy at birth, total (years) - Turkey
data_4 = quandl.get_table('WB/DATA', series_id='SP.DYN.LE00.IN', country_code='TUR')
data_4 = data_4[needed_columns]
data_4.columns = data_4.columns.str.replace("value", "life_expectancy")

# GDP per capita (current US$) - Turkey
data_5 = quandl.get_table('WB/DATA', series_id='NY.GDP.PCAP.CD', country_code='TUR')
data_5 = data_5[needed_columns]
data_5.columns = data_5.columns.str.replace("value", "GDP_in_dollars")

# Aggregate data (1960-2018)
tmp = data_1.merge(right=data_2, how="inner")
tmp2 = tmp.merge(right=data_3, how="inner")
tmp3 = tmp2.merge(right=data_5, how="inner")
data_turkey = tmp3.merge(right=data_4, how="inner")
data_turkey.to_csv("turkey_data.csv")



# Cleaning data from useless columns (year, in our case)
clean_data_turkey = pd.read_csv("turkey_data.csv", index_col=0)
clean_data_turkey.drop(["year"], axis=1, inplace=True)

coefficients_turkey, error_turkey, intervals_turkey = lr.linear_regression(clean_data_turkey)

print("Turkey:")
print(coefficients_turkey)
print(error_turkey)
print(intervals_turkey)


#########


# Urban population (% of total population) - USA
data_6 = quandl.get_table('WB/DATA', series_id='SP.URB.TOTL.IN.ZS', country_code='USA')
data_6 = data_6[needed_columns]
data_6.columns = data_6.columns.str.replace("value", "urban_population_percent")

# Fertility rate (births per woman), total (years) - USA
data_7 = quandl.get_table('WB/DATA', series_id='SP.DYN.TFRT.IN', country_code='USA')
data_7 = data_7[needed_columns]
data_7.columns = data_7.columns.str.replace("value", "fertility_rate")

# Population ages 0-14 (% of total population) - USA
data_8 = quandl.get_table('WB/DATA', series_id='SP.POP.0014.TO.ZS', country_code='USA')
data_8 = data_8[needed_columns]
data_8.columns = data_8.columns.str.replace("value", "child_population")

# Life expectancy at birth, total (years) - USA
data_9 = quandl.get_table('WB/DATA', series_id='SP.DYN.LE00.IN', country_code='USA')
data_9 = data_9[needed_columns]
data_9.columns = data_9.columns.str.replace("value", "life_expectancy")

# GDP per capita (current US$) - USA
data_10 = quandl.get_table('WB/DATA', series_id='NY.GDP.PCAP.CD', country_code='USA')
data_10 = data_10[needed_columns]
data_10.columns = data_10.columns.str.replace("value", "GDP_in_dollars")

# Aggregate data (1960-2018)
tmp = data_6.merge(right=data_7, how="inner")
tmp2 = tmp.merge(right=data_8, how="inner")
tmp3 = tmp2.merge(right=data_10, how="inner")
data_usa = tmp3.merge(right=data_9, how="inner")
data_usa.to_csv("usa_data.csv")


# Cleaning data from useless columns (year, in our case)
clean_data_usa = pd.read_csv("usa_data.csv", index_col=0)
clean_data_usa.drop(["year"], axis=1, inplace=True)

coefficients_usa, error_usa, intervals_usa = lr.linear_regression(clean_data_usa)

print("USA:")
print(coefficients_usa)
print(error_usa)
print(intervals_usa)


#########


# Urban population (% of total population) - World
data_11 = quandl.get_table('WB/DATA', series_id='SP.URB.TOTL.IN.ZS', country_code='WLD')
data_11 = data_11[needed_columns]
data_11.columns = data_11.columns.str.replace("value", "urban_population_percent")

# Fertility rate (births per woman) - World
data_12 = quandl.get_table('WB/DATA', series_id='SP.DYN.TFRT.IN', country_code='WLD')
data_12 = data_12[needed_columns]
data_12.columns = data_12.columns.str.replace("value", "fertility_rate")

# Population ages 0-14 (% of total population) - World
data_13 = quandl.get_table('WB/DATA', series_id='SP.POP.0014.TO.ZS', country_code='WLD')
data_13 = data_13[needed_columns]
data_13.columns = data_13.columns.str.replace("value", "child_population")

# Life expectancy at birth, total (years) - World
data_14 = quandl.get_table('WB/DATA', series_id='SP.DYN.LE00.IN', country_code='WLD')
data_14 = data_14[needed_columns]
data_14.columns = data_14.columns.str.replace("value", "life_expectancy")

# GDP per capita (current US$) - World
data_15 = quandl.get_table('WB/DATA', series_id='NY.GDP.PCAP.CD', country_code='WLD')
data_15 = data_15[needed_columns]
data_15.columns = data_15.columns.str.replace("value", "GDP_in_dollars")

# Aggregate data (1960-2018)
tmp = data_11.merge(right=data_12, how="inner")
tmp2 = tmp.merge(right=data_13, how="inner")
tmp3 = tmp2.merge(right=data_15, how="inner")
data_world = tmp3.merge(right=data_14, how="inner")
data_world.to_csv("world_data.csv")


# Cleaning data from useless columns (year, in our case)
clean_data_world = pd.read_csv("world_data.csv", index_col=0)
clean_data_world.drop(["year"], axis=1, inplace=True)

coefficients_world, error_world, intervals_world = lr.linear_regression(clean_data_world)

print("World:")
print(coefficients_world)
print(error_world)
print(intervals_world)


