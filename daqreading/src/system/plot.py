import matplotlib.pyplot as plt

plt.ion()

def graph(x, y, xmin = 0, xmax = 0, ymin = 0, ymax = 0, xlabel = False, ylabel = False):
    plt.plot(x, y)
    if (xmin != 0 or xmax != 0 or ymin != 0 or ymax != 0):
        plt.axis([xmin, xmax, ymin, ymax])
    if (xlabel != False):
        plt.xlabel(xlabel)
    if (ylabel != False):
        plt.ylabel(ylabel)
    plt.draw()
    plt.clf()
