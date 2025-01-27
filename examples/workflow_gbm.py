"""
This script shows the workflow for generating a Gradient Boosting Machine (GBM) model
using the landslideml library.

1. Import the library with `import landslideml as lsm`.
2. Define the main variables for the model:
    - data path
    - model type
    - target variables
    - feature list
    - test size 
3. Initialize the model with `generate_model` function.
4. Modify the model parameters with the `setup` method.
5. Predict the model with a NetCDF file using the `predict` method.

The script also shows how to save and load the model.

Note: Make sure to provide the correct data path, feature list, and test size before running.
the script.
"""

import landslideml as lsm

# Define variables for the model
DATA_PATH = "./testcase_data/training.csv"
MODEL_TYPE = "GBM"
FEATURE_LIST = ["alti",
                "slope",
                "aspect",
                "bulk_density",
                "sand",
                "usda_classes",
                "silt",
                "clay",
                "coarse_fragments",
                "avail_water_capacity",
                "land_cover",
                "tree_cover_density",
                "obs_period_max",
                "saturated_water_content",
                "alpha_mrc",
                "n_mrc"]
TARGET = 'label'
TEST_SIZE = 0.25
FILEPATH_PREDICTION = "testcase_data/prediction_cropped.nc"

# Initialize the model with the `generate_model` function
gbm = lsm.generate_model(DATA_PATH,
                         MODEL_TYPE,
                         FEATURE_LIST,
                         TARGET,
                         TEST_SIZE)

# Modify the model parameters with the `setup` method
# Note: The parameters are specific to the model type. For this example, we use the Random
# Forest parameters from scikit-learn library. Visit the scikit-learn documentation for
# more information on the parameters.
gbm.setup(n_estimators=100, max_depth=4, warm_start=True)

# Predict the model with a NetCDF file using the `predict` method
gbm.predict(FILEPATH_PREDICTION)

# Evaluate the model and show the results using the `evaluate_model` method
gbm.evaluate_model(show=True)

# Save the model using the `save_model` method
gbm.save_model("gbm_model.pkl")

# Load the model using the `load_model` function
loaded_model = lsm.load_model("gbm_model.pkl")

# Verify the loaded model by printing the prediction map
print(loaded_model.prediction_map.head())
