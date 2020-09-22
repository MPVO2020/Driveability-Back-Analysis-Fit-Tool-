# Driveability-Back-Analysis-Fit-Tool-
This Driveability Back-Analysis Fit Function tool runs via Jupyter
Notebook file (.ipynb) and calculates the Fit of the Predicted (BE and BA) Driveability and the Actual (Interpolated from Driving Logs) Driveability.

The Notebook runs the large_runfunc.py which prepares and makes some alterations
to the BE, BA and ID data. 

The Notebook then runs the eval_R_MSE function to calculate the
RMSE at individual locations.

The notebook loops through the cases and then the locations.

Documentation is provided in the Notebook and .py files. 

Further Guidance is provided in:
Driveability Back-Analysis Fit Function Instructions (v0.0)
