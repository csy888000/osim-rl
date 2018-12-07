from osim.env import L2RunEnv

from numpy import *
from walkingsim import readExcel, draw_one_data, draw_8_activation, PID, TestPID
import matplotlib.pyplot as plt

# Read muscle activation data

actList, actArray = readExcel.excel_table_byindex(startRow=23)
# for row in tableList:
#     print(row)

# print(tableMatrix)
# print(len(tableList))

print(actArray.shape)

# get simulation environment
env = L2RunEnv(visualize=True)
env.list_elements()

observation = env.reset()

numStep = 200
show_fig_one = True
show_fig_eight = False

WalkPid = PID.IncrementalPID(8, 0.5, 0.1)
IncrementalXaxis = [0]
IncrementalYaxis = [0]

# draw_8 a specific data
range_of_y_axis = [-50, 50]
draw_one_data.set_one_figure(numStep, show_fig_one, range_of_y_axis)

# draw_8 muscle activations
if show_fig_eight:
    subfigure_list = draw_8_activation.set_8_figure(numStep, show_fig_eight)
    line_name = []
    for num_line in range(len(subfigure_list)):
        locals()['line_fig_' + str(num_line)] = draw_8_activation.DrawLine(subfigure_list[num_line])
        line_name.append(locals()['line_fig_' + str(num_line)])

else:
    subfigure_list = []
    line_name = []

hip_retract = 0
for i in range(numStep):

    # muscleActivation = env.action_space.sample()
    # MH(knee flexor/hip extensor), VL (hip flexor/knee extensor)
    # MG (knee flexor/ankle plantarflexor, TA (the main ankle dorsiflexor)
    # muscleActivation = array([i/numStep, 0, 0, 0.7, 0, 0, 0, 0, 0, i/numStep, 0, 0, 0.7, 0, 0, 0, 0, 0])

    #right\left
    # hip_retract = 1
    # if i > 20:
    #     hip_retract = 1
    #     muscleActivation = array([0, 0, 0, 1, 0, 0, 0, 0, 0,
    #                           0, actArray[i][4], 0, 0, 0, actArray[i][3], actArray[i][2], 0, actArray[i][1]])
    # else:
    #     muscleActivation = array([0, actArray[i][8], 0, 0, 0, actArray[i][7], actArray[i][6], 0, actArray[i][5],
    #                           0, actArray[i][4], 0, 0, 0, actArray[i][3], actArray[i][2], 0, actArray[i][1]])

    # print(observation)

    # pelvis_height = env.get_state_desc()["body_pos"]["pelvis"][1]
    # print(pelvis_height)
    # pelvis_height = env.get_state_desc()["joint_pos"]["ground_pelvis"]
    # print(pelvis_height)
    # show_data = [x*180/3.1415 for x in env.get_state_desc()["joint_pos"]["hip_r"]]
    show_data = env.get_state_desc()["joint_pos"]["ground_pelvis"][0]*180/3.1415

    PID_out = TestPID.PID_run(WalkPid, 2, show_data)
    if show_data > 0:
        hip_retract = -PID_out / 10000
        hip_flex = 0
        muscleActivation = array([0, 0, hip_flex, hip_retract, 0, 0, 0, 0, 0,
                                  0, 0, hip_flex, hip_retract, 0, 0, 0, 0, 0])
    else:
        hip_flex = 0.1
        hip_retract = 0
        muscleActivation = array([0, 0, hip_flex, hip_retract, 0, 0, 0, 0, 0,
                                  0, 0, hip_flex, hip_retract, 0, 0, 0, 0, 0])

    observation, reward, done, info = env.step(muscleActivation)

    print(show_data, -PID_out/10000)

    # print('\n')
    # print(env.get_prev_state_desc()["joint_pos"])
    # print(env.get_observation())
    # print(env.reward())
    if show_fig_one:
        draw_one_data.draw_one(i, show_data)

    if show_fig_eight:
        draw_8_activation.draw_8(i, actArray[i, 1:9], subfigure_list, line_name)

# plt.figure(1)  # fig 1
# plt.plot(IncrementalXaxis, IncrementalYaxis, 'r')
# plt.xlim(0, numStep)
# plt.ylim(0, numStep)


