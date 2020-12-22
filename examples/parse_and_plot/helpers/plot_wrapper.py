from matplotlib import pyplot
from scipy.stats import linregress
from numpy import mean, round
from collections import Counter
from eff_snr.constants import cqi_to_sinr_thresholds

def plot(results, text, title, xlabel, ylabel, isCqi=False):
    if len(results) > 0:
        f = pyplot.figure()
        ax = f.add_subplot(111)
        bins = 1260
        weights=None

        if isCqi:
            bins = 15
            weights = 1/list(Counter(results).values())

        pyplot.hist(results, bins=bins, weights=weights)

        pyplot.xlabel(xlabel)
        pyplot.ylabel(ylabel)
        pyplot.text(0.01, 1.01, text, horizontalalignment='left',
                    verticalalignment='center', transform=ax.transAxes)
        savefig_name = title + '.png'

        pyplot.savefig(savefig_name)
        pyplot.clf()
        pyplot.close(f)


def scatter_plot(punctured_sc, results, text, title, xlabel, ylabel):
    if len(results) > 0:
        f = pyplot.figure()
        ax = f.add_subplot(111)

        mean_y = []
        for i in range(0, len(results)):
            mean_y.append(mean(results[i]))

        slope, intercept, r_value, p_value, std_err = linregress(punctured_sc, mean_y)
        comment = "$y={0}x+{1}, std.err:{2}$".format(round(slope, 5), round(intercept, 2), round(std_err, 4))

        x_min = punctured_sc[0]
        x_max = punctured_sc[len(punctured_sc) - 1]
        x = [i for i in range(x_min, x_max)]

        y = []
        for i in range(0, len(x)):
            y.append(x[i] * slope + intercept)
        pyplot.scatter(x, y, s=0.5)

        for xe, ye in zip(punctured_sc, results):
            pyplot.scatter([xe] * len(ye), ye)

        pyplot.xlabel(xlabel)
        pyplot.ylabel(ylabel)
        pyplot.grid(True)
        pyplot.text(0.01, 1.01, comment, horizontalalignment='left',
                    verticalalignment='center', transform=ax.transAxes)
        savefig_name = title + '.png'

        cqi_res = []
        for i in range(0, len(x)):
            cqi = '0'
            for cqi_snr_thresh in cqi_to_sinr_thresholds.keys():
                # lin_snr_thresh = power(10,  / 10)
                if cqi_to_sinr_thresholds[cqi_snr_thresh] < x[i] * slope + intercept:
                    cqi = cqi_snr_thresh
            cqi_res.append(cqi)

        ax2 = ax.twinx()
        ax2.grid(True, alpha=0.6, color='lightcyan')
        f.gca().invert_yaxis()
        ax2.set_ylabel("CQI", color='navy')
        ax2.scatter(x, cqi_res, s=0.5, color='navy')

        pyplot.savefig(savefig_name)
        pyplot.clf()
        pyplot.close(f)

