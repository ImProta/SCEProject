"""A module for creating and training machine learning models for landslide prediction.

This module provides a class called `model` which allows users to create and train
machine learning models for landslide prediction. The module supports two types of 
models: RandomForest and SVM. Users can specify the model type, filepath to the dataset, 
test size for train-test split, and other optional parameters.

"""

import os
import warnings
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from landslideml import VALID_MODELS

class MlModel:
    """
    A class for creating and training machine learning models for landslide prediction.

    Attributes:
        model_type (str): The type of machine learning model to be used. Supported model types are 
            'RandomForest', 'SVM', and 'GBM'.
        filepath (str): The filepath of the dataset to be used for training and testing the model.
        target (str): The target variable in the dataset.
        features (list): The list of feature variables in the dataset.
        test_size (float): The proportion of the dataset to be used for testing the model.
        kwargs (dict): Additional keyword arguments to be passed to the machine learning model.
        type (str): The type of machine learning model.
        model: The initialized machine learning model.
        dataset: The loaded dataset.
        x_train: The training set features.
        x_test: The testing set features.
        y_train: The training set target variable.
        y_test: The testing set target variable.

    Args:
        model_type (str): The type of machine learning model to be used. Supported model types are 
            'RandomForest', 'SVM', and 'GBM'.
        filepath (str): The filepath of the dataset to be used for training and testing the model.
        target (str): The target variable in the dataset.
        features (list): The list of feature variables in the dataset.
        test_size (float): The proportion of the dataset to be used for testing the model.
        **kwargs: Additional keyword arguments to be passed to the machine learning model.

    Raises:
        ValueError: If the model type is not supported.
        TypeError: If the filepath is not a string, the target is not a string, the features
            are not a list, or the features are not strings.
    """

    def __init__(self,
                  filepath=None,
                  model_type='RandomForest',
                  target_column='label',
                  features_list=None,
                  test_size=0.2,
                  **kwargs):
        self.__verify_input(model_type, filepath, target_column, features_list, test_size)
        self.filepath = filepath
        self.type = model_type
        self.target_column = target_column
        self.features_list = features_list
        self.test_size = test_size
        self.kwargs = kwargs['kwargs']
        # Load and preprocess the dataset
        self.__load_dataset()
        self.__preprocess_data()
        self.model = self.__initialize_model()

        # Initialize the model attributes
        self.y_pred = None
        self.report = None
        self.last_prediction = None

    def __initialize_model(self):
        """
        Initialize the machine learning model based on the specified model type.
        """
        if self.type == 'RandomForest':
            return RandomForestClassifier(**self.kwargs)
        elif self.type == 'SVM':
            return SVC(**self.kwargs)
        elif self.type == 'GBM':
            return GradientBoostingClassifier(**self.kwargs)
        else:
            raise ValueError('Model type not supported.')

    def __load_dataset(self):
        """
        Load the data from the specified filepath.
        """
        self.dataset = pd.read_csv(self.filepath, header=0)

    def __preprocess_data(self):
        """
        Preprocess the data by splitting it into training and testing sets.
        """
        x = self.dataset[self.features_list]
        y = self.dataset[self.target_column]
        self.x_train, self.x_test, self.y_train, self.y_test = train_test_split(
            x, y, test_size=self.test_size, random_state=42)

    def __verify_input(self, model_type, filepath, target, features, test_size):
        """
        Verify the input arguments for the model.
        """
        if model_type not in VALID_MODELS:
            raise ValueError('Model type not supported.')
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"File '{filepath}' does not exist.")
        if not isinstance(target, str):
            raise TypeError('Target must be a string.')
        if not isinstance(features, list):
            raise TypeError('Features must be a list.')
        if not all(isinstance(feature, str) for feature in features):
            raise TypeError('Features must be a list of strings.')
        if not isinstance(test_size, float):
            raise TypeError('Test size must be a float.')
        if test_size <= 0 or test_size >= 1:
            raise ValueError('Test size must be between 0 and 1.')

    def setup(self, **kwargs):
        """
        Reconfigure the model with new parameters.

        Args:
            **kwargs: Keyword arguments to be passed to the machine learning model.
        """
        # Check if the given kwargs are within the allowed kwargs for the model
        invalid_kwargs = [kwarg for kwarg in kwargs if kwarg not in self.model.get_params()]
        if invalid_kwargs:
            raise ValueError(f"Invalid kwargs found: {', '.join(invalid_kwargs)}")
        # Update the kwargs with the new parameters
        self.kwargs.update(kwargs)
        # Reinitialize the model with the updated kwargs
        self.model = self.__initialize_model()
        self.model.fit(self.x_train, self.y_train)
        self.y_pred = self.model.predict(self.x_test)

    def evaluate_model(self, *, plot=False):
        """
        Evaluate the performance of the trained model.
        """
        if self.y_pred is None:
            warnings.warn("No data was loaded. Prediction will be done with test data.")
            self.y_pred = self.model.predict(self.x_test)
        if plot is True:
            print(classification_report(self.y_test, self.y_pred, output_dict=False))
        self.report = classification_report(self.y_test, self.y_pred, output_dict=True)
        return self.report

    def predict(self, data):
        """
        Make predictions using the trained model.

        Args:
            x (array-like): The input features for making predictions.

        Returns:
            array: The predicted values.
        """
        self.last_prediction = self.model.predict(data)
        return self.model.predict(data)