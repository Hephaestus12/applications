"""
  @file model.py
  @author Tej Sukhatme

  Linear Ridge Regression.
"""
import pickle
import shogun as sg

from src import clean
from src import combine
from src import config
from src import process
from src import util


class Model:
    def __init__(self):
        self.random_forest = {}
        self.cleaner = clean.Cleaner()
        self.processor = process.Processor()
        self.combiner = combine.Combiner()

    def train(self):
        self.combiner.combine_data()
        self.cleaner.clean_data()
        self.processor.process_data()

        for country in config.COUNTRIES:
            x_train_file_path = config.processed_data_path / (
                    country + '_features.csv')
            y_train_file_path = config.processed_data_path / (
                        country + '_labels.csv')

            features_train = sg.create_features(util.load(x_train_file_path).T)
            labels_train = sg.create_labels(
                    util.load(y_train_file_path, is_labels=True))

            mean_rule = sg.create_combination_rule("MeanRule")
            rand_forest = sg.create_machine("RandomForest",
                                            labels=labels_train,
                                            num_bags=5, seed=1,
                                            combination_rule=mean_rule)

            rand_forest.train(features_train)

            model_file_path = config.models_path / (country+'_model.pkl')
            pickle.dump(rand_forest,
                        open(str(model_file_path.absolute()), "wb"))

            self.random_forest[country] = rand_forest

    def apply(self, country, pageviews):
        self.cleaner.clean_vector(pageviews)
        data = self.processor.process_vector(pageviews, country)

        # apply trained model on data
        features_test = sg.create_features(data.values().T)
        labels_predict = self.random_forest[country].apply_regression(
                features_test)
        prediction = labels_predict.get("labels")
        return prediction

