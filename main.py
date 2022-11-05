import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import input_reader as inp
import prediction_model as pred

path = "calibration.csv"
l_value = 1
original_concentration = 50

calibration_sample = inp.sample(path, l_value)

blanks, calibrations = calibration_sample.read_clean()
lambdas = calibration_sample.lambdas
dilutions = calibration_sample.dilutions

calibration_sample.plot_raw(calibrations)
calibration_sample.plot_corrected(calibrations, blanks)

model = pred.model(l_value)

model.fit_E(calibrations, blanks, original_concentration, dilutions, lambdas)



print()




