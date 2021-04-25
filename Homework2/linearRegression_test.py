import unittest
import pandas as pd

from Homework2 import linearRegression as lr

df = pd.read_csv("bad_data.csv", index_col=0)
df.drop(["year"], axis=1, inplace=True)

empty_df = pd.DataFrame()

df_one_column = df[df.columns[0]]


class LinearRegressionTest(unittest.TestCase):

    def test_nan(self):
        self.assertIsNotNone(lr.linear_regression(df))

    def test_empty(self):
        self.assertIsNone(lr.linear_regression(empty_df))

    def test_not_dataframe(self):
        self.assertIsNone(lr.linear_regression(df_one_column))

    def test_non_numeric(self):
        self.assertIsNotNone(lr.linear_regression(df))


if __name__ == "__main__":
    unittest.main()

