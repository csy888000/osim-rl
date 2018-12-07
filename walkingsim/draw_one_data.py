import numpy as np
import matplotlib.pyplot as plt
from math import *


def set_one_figure(num_step, show_data=True, rangeyaxis=[-1, 1]):
    range_low = rangeyaxis[0]
    range_high = rangeyaxis[1]
    if show_data:
        plt.ion()

        fig = plt.figure(num=1)
        ax1 = fig.add_subplot(111)

        ax1.set_title('Real-time Data')
        plt.xlabel('Frame')
        plt.ylabel('Y')
        plt.axis([0, num_step, range_low, range_high])


def draw_one(x, y, show_data=True):
    if show_data:
        plt.scatter(x, y, c='b', marker='.')
        plt.pause(0.0001)


# for i in range(100):
#     y = sin(i*0.1)
#     plt.scatter(i, y, c='b', marker='.')
#     plt.pause(0.05)