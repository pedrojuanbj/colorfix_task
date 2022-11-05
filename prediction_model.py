import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class model():
    def __init__(self, l_value):
        self.l = l_value

    def get_E(self, concentration, absorbance):
        E = absorbance / (concentration * self.l)
        return E

    def predict_C(self, absorbance, E_coeff):
        C = absorbance / (E_coeff * self.l)
        return C

    def rmse(self, predictions, targets):
        return np.sqrt(((predictions - targets) ** 2).mean())

    def fit_E(self, data, data_blank, original_C, dilutions, lambdas):

        blanks = np.mean(data_blank, axis=0)
        concentrations = original_C / dilutions
        all_E_values = []
        for n, l in enumerate(lambdas):
            E_values = []
            measurements = data.loc[data["Sample"] == "S1"]
            for c, d in zip(concentrations, dilutions):
                samples = measurements.loc[measurements["Dilution"] == d][l] - blanks[n]
                E = self.get_E(c, samples)
                E_values.append(E)
            all_E_values.append(np.mean(E_values))

        predicted_Cs = []
        for n, l in enumerate(lambdas):
            C_values = []
            measurements = data.loc[data["Sample"] == "S1"]
            for c, d in zip(concentrations, dilutions):
                samples = measurements.loc[measurements["Dilution"] == d][l] - blanks[n]
                C = self.predict_C(samples, all_E_values[n])
                C_values.append(C)
            predicted_Cs.append(C_values)

        accuracies_at_lambdas = []
        for n, l in enumerate(lambdas):
            pred = predicted_Cs[n]
            acc_at_Cs = []
            for c_pred, c_og in zip(pred, concentrations):
                accuracy = self.rmse(np.mean(c_pred), c_og)
                acc_at_Cs.append(accuracy)
            accuracies_at_lambdas.append(np.mean(acc_at_Cs))

        best = np.nanargmin(accuracies_at_lambdas)
        print("Model found best lambda to predict concentration at: ", lambdas[best])

        return all_E_values, predicted_Cs, accuracies_at_lambdas
