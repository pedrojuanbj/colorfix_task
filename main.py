import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import input_reader as inp
import prediction_model as pred

path = "calibration.csv"
l_value = 1
original_concentration = 50

#Reading the sample from the calibration
calibration_sample = inp.sample(path, l_value)

blanks, calibrations = calibration_sample.read_clean(blank_val="Blank", sample_val="S1")

#We can retrieve the lambdas and dilutions used
lambdas = calibration_sample.lambdas
dilutions = calibration_sample.dilutions

#We now plot the original sample data and the blank-corrected data
calibration_sample.plot_raw(calibrations)
calibration_sample.plot_corrected(calibrations, blanks)


#With this we can fit a model to predict concentrations
model = pred.model(l_value)

#Using the data, we fit the "model" to get E values at lambdas
#And also find the best lambda to be accurately predicting concentration
E_values, pred_Cs, accuracies = model.fit_E(calibrations, blanks, original_concentration, dilutions, lambdas)

#After fitting we can find the E that gives the best lambda to predict
best_idx = np.nanargmin(accuracies)

plt.plot(lambdas, accuracies, label="Predicted RMSE")
plt.plot(lambdas[best_idx], accuracies[best_idx], "o",  color="r", label="Best $\lambda$")
plt.xticks(range(0, len(lambdas))[::20], lambdas[::20], rotation=60)
plt.ylabel("Root Mean Squared Error (RMSE)")
plt.xlabel("Wavelengths ($\lambda$)")
plt.legend()
plt.tight_layout()
plt.savefig("best_rmse_lambda.png")
plt.show()

best_lmbd = lambdas[best_idx]

#We now read in the data
exp_path = "sample.csv"
experimental_sample = inp.sample(exp_path, l_value)
exp_blanks, samples = experimental_sample.read_clean(blank_val="Blank", sample_val="X1")
blank_exp = np.mean(exp_blanks[best_lmbd])

#Prediction for the samples
for sample in (samples[best_lmbd] - blank_exp):
    print("Concentration is ", model.predict_C(sample, E_values[best_idx]))

print()




