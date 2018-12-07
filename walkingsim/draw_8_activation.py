import numpy as np
import matplotlib.pyplot as plt


class DrawLine:
    def __init__(self, fig_handle):
        self.t = []
        self.m = []
        self.fig_handle = fig_handle

    def draw_fig(self, x, y, fig_handle, line_type):
        plt.sca(fig_handle)
        self.t.append(x)
        self.m.append(y)
        plt.plot(self.t, self.m, line_type)
        plt.draw()

    def get(self):
        return self.t, self.m


def set_8_figure(num_step, show_figure=True):
    if show_figure:
        plt.figure(num=8, figsize=(5, 10))

        plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.05, wspace=0.2, hspace=0.3)

        ax1 = plt.subplot(811)
        plt.xlim((0, num_step))
        plt.ylim((0, 1))
        plt.title('Activation(Blue=Left/Red=Right)')
        # plt.xlabel('Plot Number')
        plt.ylabel('TA_left\nAnkle flexor')
        ax2 = plt.subplot(812, sharex=ax1, sharey=ax1)
        plt.ylabel('MG_left\nAnkle extensor')
        ax3 = plt.subplot(813, sharex=ax1, sharey=ax1)
        plt.ylabel('VL_left\nKnee extensor')
        ax4 = plt.subplot(814, sharex=ax1, sharey=ax1)
        plt.ylabel('BF_left\nKnee flexor')
        ax5 = plt.subplot(815, sharex=ax1, sharey=ax1)
        plt.ylabel('TA_right\nAnkle flexor')
        ax6 = plt.subplot(816, sharex=ax1, sharey=ax1)
        plt.ylabel('MG_right\nAnkle extensor')
        ax7 = plt.subplot(817, sharex=ax1, sharey=ax1)
        plt.ylabel('VL_right\nKnee extensor')
        ax8 = plt.subplot(818, sharex=ax1, sharey=ax1)
        plt.ylabel('BF_right\nKnee flexor')
        subfigure_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]
    return subfigure_list


def draw_8(x, activation_data, subfigure_list, line_name, show_figure=True):
    if show_figure:
        for num_name in range(len(line_name)):
            if num_name < 4:
                line_type = '-b'
            else:
                line_type = '-r'
            line_name[num_name].draw_fig(x, activation_data[num_name], subfigure_list[num_name], line_type)
        plt.pause(0.0001)


# plt.show()

