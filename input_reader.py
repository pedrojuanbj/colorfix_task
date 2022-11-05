import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class sample():
    def __init__(self, path, l_value):
        self.path = path
        self.l = l_value

    def read_clean(self):

        raw_data = pd.read_csv(self.path, skiprows=range(0,10), delimiter=",")
        self.wells = raw_data["Well"]
        self.samples = raw_data["Sample"]
        self.dilutions = raw_data["Dilution"]
        self.lambdas = raw_data.iloc[:, 3:].columns

        blank_data = raw_data.loc[raw_data["Sample"] == "Blank"]
        samples_data = raw_data.loc[raw_data["Sample"] == "S1"]

        return blank_data, samples_data

    def plot_raw(self, samples_data):
        values = samples_data.iloc[:, 3:].to_numpy()

        plt.figure(figsize=(8, 2))
        plt.title("Absorbance of S1 samples")
        for n, well in enumerate(values):
            plt.plot(self.lambdas, well, color="r", label="Sample S1" if n == 0 else "", alpha=0.1)
        plt.xticks(range(0, len(self.lambdas))[::10], self.lambdas[::10], rotation=60)
        plt.ylabel("Absorbance Value")
        plt.xlabel("Wavelengths ($\lambda$)")
        plt.legend()
        plt.show()

        return

    def plot_corrected(self, samples_data, blank_data):
        values = samples_data.iloc[:, 3:].to_numpy()
        blank_values = blank_data.iloc[:, 3:].to_numpy()
        blanks = np.mean(blank_values, axis=0)

        plt.figure(figsize=(8, 2))
        plt.title("Absorbance of S1 samples Blank Corrected")
        for n, well in enumerate(values - blanks):
            plt.plot(self.lambdas, well, color="r", label="Sample S1" if n == 0 else "", alpha=0.1)
        plt.xticks(range(0, len(self.lambdas))[::10], self.lambdas[::10], rotation=60)
        plt.ylabel("Absorbance Value")
        plt.xlabel("Wavelengths ($\lambda$)")
        plt.legend()
        plt.show()

        return