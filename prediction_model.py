import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class model():
    """
    Model class for "fitting" data to calculate the E coefficient for every measurement and then try to predict the
    concentration back for each E, finding thus the best lambda/E to predict back the concentration accurately.
    """
    def __init__(self, l_value):
        """
        Initializing class, need l_value used on the measurement
        :param l_value: (float) Value for the l used when measuring the SOP
        """
        self.l = l_value

    def get_E(self, concentration, absorbance):
        """
        Calculate the E coefficient for any given pair of concentration and absorbance measured

        :param concentration: (float or list) Measured concentrations
        :param absorbance: (float or list) Measured absorbances for each known concentration for a given wavelength
        :return:(float or list) E value calculated at each pair of A/C
        """
        E = absorbance / (concentration * self.l)
        return E

    def predict_C(self, absorbance, E_coeff):
        """
        Equation to predict the concentration using absorbance and an E coefficient
        :param absorbance: (float or list) abosrbance measured for the given wavelength
        :param E_coeff: (float or list) E coefficient for the given wavelength
        :return: (float or list) Predicted concentration
        """
        C = absorbance / (E_coeff * self.l)
        return C

    def rmse(self, predictions, targets):
        """
        Small Root Mean Squared Error calculator function
        :param predictions: (float or list) predicted concentration values
        :param targets: (float or list) experimental values as targets
        :return: (float) Overall RMSE of the given data
        """
        return np.sqrt(((predictions - targets) ** 2).mean())

    def fit_E(self, data, data_blank, original_C, dilutions, lambdas):
        """
        Method to "fit" the data, which means calculating the E values for each concentration/wavelength and then use it
        to repredict the given concentrations. After doing so, the best wavelength is picked to be the best and a plot
        shows the RMSE error for each wavelength measured, thus finding the most correlated to use for prediction.
        :param data: (DataFrame) Experimental data
        :param data_blank: (DataFrame) Blanks for the given experimental data
        :param original_C: (float) Original concentration for the dilution factors
        :param dilutions: (list) Dilution factors
        :param lambdas: (list) List of lambdas used for the measurements
        :return: (all_E_values, predicted_Cs, accuracies_at_lambdas) Returns calculated E coefficients, the predicted
            concentrations for each E value, and the accuracies for each lambda/E.
        """

        blank_values = data_blank.iloc[:, 3:].to_numpy()
        blanks = np.mean(blank_values, axis=0)
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
