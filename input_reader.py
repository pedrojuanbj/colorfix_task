import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class sample():
    """
    Sample class to store information on the single measurement data that cleans the data and separates blank from
    sample values for a given sample name and blank name. It has also methods to plot the raw data and the blank
    corrected data

    """

    def __init__(self, path, l_value):
        """
        Initialize with path and l_value for the SOP
        :param path: (str) Path to the file
        :param l_value: (float) Value for the l used when measuring the SOP
        """
        self.path = path
        self.l = l_value

    def read_clean(self, blank_val, sample_val):
        """
        Method to read in the data from the file, specific for CSV using pandas

        :param blank_val:  (str) Value to use when locating the desired blank sample measured
        :param sample_val: (str) Value to use when locating the desired experimental sample measured
        :return: [blank_data, samples_data]
        """

        raw_data = pd.read_csv(self.path, skiprows=range(0,10), delimiter=",")
        self.wells = raw_data["Well"]
        self.samples = raw_data["Sample"]
        self.dilutions = np.unique(raw_data["Dilution"])
        self.lambdas = raw_data.iloc[:, 3:].columns

        blank_data = raw_data.loc[raw_data["Sample"] == blank_val]
        samples_data = raw_data.loc[raw_data["Sample"] == sample_val]

        return blank_data, samples_data

    def plot_raw(self, samples_data):
        """
        Function for plotting the raw values from a sample

        :param samples_data: (DataFrame) Experimental Values to plot
        :return:
        """
        values = samples_data.iloc[:, 3:].to_numpy()

        plt.figure(figsize=(8, 2))
        plt.title("Absorbance of S1 samples")
        for n, well in enumerate(values):
            plt.plot(self.lambdas, well, color="r", label="Sample" if n == 0 else "", alpha=0.1)
        plt.xticks(range(0, len(self.lambdas))[::10], self.lambdas[::10], rotation=60)
        plt.ylabel("Absorbance Value")
        plt.xlabel("Wavelengths ($\lambda$)")
        plt.legend()
        plt.tight_layout()
        plt.savefig("raw.png")
        plt.show()

        return

    def plot_corrected(self, samples_data, blank_data):
        """
        Function to correct and plot values from some data

        :param samples_data: (DataFrame) Experimental Values to correct and plot
        :param blank_data: (DataFrame) Experimental Values for the blank to correct with
        :return:
        """
        values = samples_data.iloc[:, 3:].to_numpy()
        blank_values = blank_data.iloc[:, 3:].to_numpy()
        blanks = np.mean(blank_values, axis=0)

        plt.figure(figsize=(8, 2))
        plt.title("Absorbance of S1 samples Blank Corrected")
        for n, well in enumerate(values - blanks):
            plt.plot(self.lambdas, well, color="r", label="Sample" if n == 0 else "", alpha=0.1)
        plt.xticks(range(0, len(self.lambdas))[::10], self.lambdas[::10], rotation=60)
        plt.ylabel("Absorbance Value")
        plt.xlabel("Wavelengths ($\lambda$)")
        plt.legend()
        plt.tight_layout()
        plt.savefig("corrected.png")
        plt.show()

        return