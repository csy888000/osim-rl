import numpy as np
import matplotlib.pyplot as plt
from math import *


class DrawFig:
    def __init__(self, show_data):
        self.t = []
        self.m = []
        # self.fig_handle = fig_handle
        self.fig_num = 1
        self.show_data = show_data
        self.fig_handle = []
        self.subfigure_list = []
        self.line_name = []
        self.t_time = [[] for i in range(8)]
        self.m_muscle = [[] for i in range(8)]

    def set_fig_handle(self, fig_handle):
        self.fig_handle = fig_handle
        # return self.fig_handle

    def set_fig(self, range_y_axis, num_step=200):

        if self.show_data:
            # plt.ion()

            fig = plt.figure(self.fig_num)
            fig_handle = fig.add_subplot(111)

            plt.axis([0, num_step, range_y_axis[0], range_y_axis[1]])
        else:
            fig_handle = []
        return fig_handle

    def draw_fig(self, muscle_x, muscle_y, fig_handle, line_type='b.'):
        plt.sca(fig_handle)
        self.t.append(muscle_x)
        self.m.append(muscle_y)
        plt.plot(self.t, self.m, line_type)
        plt.draw()

    def clear_fig(self):
        plt.cla()

    def get(self):
        return self.t, self.m


class DrawOne(DrawFig):
    def set_fig(self, range_y_axis=[-1, 1], num_step=200):
        if self.show_data:
            # plt.ion()
            self.fig_num = 1
            fig = plt.figure(self.fig_num)
            fig_handle = fig.add_subplot(111)

            fig_handle.set_title('Real-time Data')
            plt.xlabel('Frame')
            plt.ylabel('Y')
            # plt.axis([0, num_step, range_y_axis[0], range_y_axis[1]])
            plt.xlim(0, num_step)
            plt.ylim(range_y_axis[0], range_y_axis[1])
        else:
            fig_handle = []
        return fig_handle

    def draw_one(self, x, y, show_data=True):
        if self.show_data:
            plt.scatter(x, y, c='b', marker='.')
            plt.pause(0.0001)
            plt.autoscale(enable=True, axis='y', tight=None)


class DrawTwo(DrawFig):
    def set_fig_2(self):
        if self.show_data:
            # plt.ion()
            self.fig_num = 1
            fig_two = plt.figure(self.fig_num)
            self.fig_handle = fig_two.add_subplot(111)
            # fig_handle = plt.subplot(111)

            self.fig_handle.set_title('Real-time Data')
            plt.xlabel('Frame')
            plt.ylabel('Y')
            # plt.axis([0, num_step, range_y_axis[0], range_y_axis[1]])
            plt.xlim(0, 200)
        else:
            self.fig_handle = []
        return self.fig_handle

    def set_fig_2_xlim(self, num_step=200):
        if self.show_data:
            if num_step > 200:
                plt.xlim(0, num_step)
            else:
                plt.xlim(0, 200)

    def draw_two(self, x, y, y2, i):
        if self.show_data:
            plt.sca(self.fig_handle)
            self.set_fig_2_xlim(i)
            plt.scatter(x, y, c='b', marker='.')
            plt.scatter(x, y2, c='r', marker='o')

            plt.autoscale(enable=True, axis='y', tight=None)
            plt.pause(0.01)
            # plt.savefig('Real-TimeData.png')
            # plt.ioff()


class DrawEight(DrawFig):
    def set_figure_8(self, num_step=200):
        if self.show_data:
            plt.figure(num=8, figsize=(5, 10))
            plt.subplots_adjust(left=0.15, right=0.95, top=0.95, bottom=0.05, wspace=0.2, hspace=0.3)

            ax1 = plt.subplot(811)
            plt.xlim(0, num_step)
            plt.ylim(0, 1)
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
            self.subfigure_list = [ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8]
        else:
            self.subfigure_list = []
        return self.subfigure_list

    def draw_8(self, step_n, activation_data, subfigure_list):
        if self.show_data:
            for num_name in range(len(subfigure_list)):
                if num_name < 4:
                    line_type = '-b'
                else:
                    line_type = '-r'
                # print(step_n)
                # print(activation_data)
                # print(self.subfigure_list)
                # print(line_type)
                self.draw_fig_8(num_name, step_n, activation_data[num_name], line_type)
        plt.pause(0.0001)

    def draw_fig_8(self, num_muscle, muscle_x, muscle_y, line_type='b.'):
        plt.sca(self.subfigure_list[num_muscle])
        self.t_time[num_muscle].append(muscle_x)
        self.m_muscle[num_muscle].append(muscle_y)
        plt.plot(self.t_time[num_muscle], self.m_muscle[num_muscle], line_type)
        # plt.scatter(muscle_x, muscle_y, c='b', marker='.')
        plt.draw()


if __name__ == '__main__':
    x = np.linspace(0, 2 * np.pi, 50)
    OneFig = DrawTwo(True)
    ax00 = DrawTwo.set_fig_2(OneFig, 10)
    DrawTwo.draw_two(OneFig, x, np.sin(x), np.sin(x)+1)
