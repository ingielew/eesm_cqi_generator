from matplotlib import pyplot
from scipy.stats import linregress
from numpy import mean, round


def plot(results, text, title, xlabel, ylabel):
    if len(results) > 0:
        f = pyplot.figure()
        ax = f.add_subplot(111)

        pyplot.hist(results, bins=630)

        pyplot.xlabel(xlabel)
        pyplot.ylabel(ylabel)
        pyplot.text(0.01, 1.01, text, horizontalalignment='left',
                    verticalalignment='center', transform=ax.transAxes)
        savefig_name = title+'.png'

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
        comment = "$y={0}x+{1}, std.err:{2}$".format(round(slope, 2), round(intercept, 2), round(std_err,3))

        x_min = punctured_sc[0]
        x_max = punctured_sc[len(punctured_sc)-1]
        x = [i for i in range(x_min, x_max)]

        y = []
        for i in range(0, len(x)):
            y.append(x[i]*slope+intercept)
        pyplot.scatter(x, y, s=0.5)

        for xe, ye in zip(punctured_sc, results):
            pyplot.scatter([xe]*len(ye), ye)

        pyplot.xlabel(xlabel)
        pyplot.ylabel(ylabel)
        pyplot.text(0.01, 1.01, comment, horizontalalignment='left',
                    verticalalignment='center', transform=ax.transAxes)
        savefig_name = title+'.png'

        pyplot.savefig(savefig_name)
        pyplot.clf()
        pyplot.close(f)
