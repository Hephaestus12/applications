"""
  @file process.py
  @author Tej Sukhatme

  Data pre-processing.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats
from scipy.stats import skew


def process_data():
    path = Path.cwd()
    cleaned_data_path = path.parent / 'data' / 'cleaned'
    processed_data_path = path.parent / 'data' / 'processed'
    countries = ['austria', 'belgium', 'germany', 'italy', 'netherlands']
    df = {}
    lmbda = {'austria'    : {}, 'belgium': {}, 'germany': {}, 'italy': {},
             'netherlands': {}}
    for country in countries:
        # read file
        file_path = cleaned_data_path / (country + '.csv')
        df[country] = pd.read_csv(file_path)

        add_polynomial_features(country, df, 10)

        # separate numerical features from categorical ones
        numerical_features = df[country].select_dtypes(
                exclude=["object"]).columns
        numerical_features = numerical_features.drop('incidence')

        # skewness of >0.5 can be considered to be moderately skewed.
        skewness = df[country][numerical_features].apply(lambda x: skew(x))
        skewness = skewness[abs(skewness) > 0.5]
        skewed_features = skewness.index
        train_leo_johnson(df[country], lmbda[country], skewed_features)

        means = {}
        std_deviations = {}
        train_std_normal(df[country], numerical_features, means,
                         std_deviations)

        # apply yeo johnson to incidence too
        train_leo_johnson(df[country], lmbda[country], ['incidence'])

        hot_encode_weeks(country, df)

        # save to file.
        processed_file_path = processed_data_path / (country + '.csv')
        df[country].to_csv(processed_file_path, index=False)


# perform one hot encoding for week numbers
def hot_encode_weeks(country, df):
    week_number = []
    for index, row in df[country].iterrows():
        week_number.append(row['week'][-2:])
    df[country]['week_number'] = week_number
    one_hot_encoded_weeks = pd.get_dummies(df[country]['week_number'],
                                           prefix='week')
    df[country] = pd.concat([df[country], one_hot_encoded_weeks], axis=1)
    df[country].drop(columns=['week_number'])


# we transform features so that mean is 0 and std deviation is 1.
def apply_std_normal(df, numerical_features, means, std_deviations):
    for feature in numerical_features:
        column = df[feature]
        column -= means[feature]
        column /= std_deviations[feature]
        df[feature] = column


# we transform features so that mean is 0 and std deviation is 1.
def train_std_normal(df, numerical_features, means, std_deviations):
    for feature in numerical_features:
        column = df[feature]
        means[feature] = column.mean()
        std_deviations[feature] = column.std()
        column -= means[feature]
        column /= std_deviations[feature]
        df[feature] = column


# we apply the Yeo Johnson Transformation.
def apply_leo_johnson(df, lmbda, skewed_features):
    for feature in skewed_features:
        column = df[feature] + 1
        column = stats.boxcox(column, lmbda=lmbda[feature])
        column = pd.Series(column)
        df[feature] = column


# we train AND apply the Yeo Johnson Transformation.
def train_leo_johnson(df, lmbda, skewed_features):
    for feature in skewed_features:
        column = df[feature] + 1
        column, lmbda[feature] = stats.boxcox(column)
        column = pd.Series(column)
        df[feature] = column


# add 3 polynomial features each for the most important features.
def add_polynomial_features(country, df, num):
    # find the correlation matrix.
    correlation_matrix = df[country].corr()
    correlation_matrix.sort_values(['incidence'], ascending=False,
                                   inplace=True)

    count = 0
    for column, correlation in correlation_matrix['incidence'].items():
        if count > num:
            break
        if column == 'incidence' or column == 'week' or column == 'date':
            continue
        df[country][column + '-s2'] = df[country][column] ** 2
        df[country][column + '-s3'] = df[country][column] ** 3
        df[country][column + '-sq'] = np.sqrt(df[country][column])
        count += 1


process_data()