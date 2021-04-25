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
