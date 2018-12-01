import json

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
from sklearn.linear_model import LinearRegression


class OptimizationAnalysis(object):

    def __init__(self, log_file):
        with open(log_file) as infile:
            self.results = json.load(infile)

    def get_param_coeffs(self):
        param_keys = sorted(self.results['meta']['params'].keys())

        x = []
        y = []
        for result in self.results['results']:
            x.append([result['params'][key] for key in param_keys])
            y.append(result['stats']['all']['net_profit'])

        reg = LinearRegression().fit(x, y)
        coeffs = reg.coef_
        return {param_keys[i]: coeffs[i] for i in range(len(param_keys))}

    def surface_plot(self, param1, param2):
        x = []
        y = []
        z = []
        for result in self.results['results']:
            x.append(result['params'][param1])
            y.append(result['params'][param2])
            z.append(result['stats']['all']['net_profit'])

        fig = plt.figure()
        ax = fig.gca(projection='3d')
        ax.scatter(x, y, z)
        ax.set_xlabel(param1)
        ax.set_ylabel(param2)
        ax.set_zlabel('Net profit')
        plt.show()


if __name__ == '__main__':
    analyzer = OptimizationAnalysis('/localdisk/trading/logs/followMovingAvgSlope_AAPL_30min.json')
    print(analyzer.get_param_coeffs())
    analyzer.surface_plot('abs_slope', 'stop_loss')
