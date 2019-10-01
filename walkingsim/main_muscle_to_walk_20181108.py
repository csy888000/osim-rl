from osim.env import L2RunEnv

from numpy import *
from walkingsim import readExcel, draw_data_one, draw_activation_8, PID, TestPID
import matplotlib.pyplot as plt

# Read muscle activation data
roundNum = 1
actList, actArray = readExcel.excel_table_byindex(startRow=23)

motionList, motionArray_raw = readExcel.excel_table_byindex_raw(startRow=0, file='normal_new.xls', colnameindex=0, by_index=0)
motionArray = tile(motionArray_raw, (roundNum, 1))

print(actArray.shape)
print(motionArray.shape)
# for row in motionList:
#     print(row)

# print(tableMatrix)
# print(len(tableList))


# get simulation environment
env = L2RunEnv(visualize=True)
env.list_elements()

observation = env.reset()

numStep = 201*roundNum

# show figures?
show_fig_one = False
show_fig_eight = True

for subNum in range(6):
    locals()['WalkPid' + str(subNum)] = PID.PositionalPID(5, 0, 1)  # (45, 0.7, 580) (20, 0.5, 100)
for subNum2 in range(6):
    locals()['WalkPid' + str(subNum2+6)] = PID.PositionalPID(20, 0.5, 100)  # (10, 0.8, 10)
WalkPidArray = [WalkPid0, WalkPid1, WalkPid2, WalkPid3, WalkPid4, WalkPid5]
WalkPidBackArray = [WalkPid6, WalkPid7, WalkPid8, WalkPid9, WalkPid10, WalkPid11]
BalancePid = PID.IncrementalPID(15, 0.5, 0.1)
IncrementalXaxis = [0]
IncrementalYaxis = [0]

# draw_8 a specific data


range_of_y_axis = [-90, 90]
draw_data_one.set_figure_one(numStep, show_fig_one, range_of_y_axis)
# draw_8 muscle activations
if show_fig_eight:
    subfigure_list = draw_activation_8.set_8_figure(numStep, show_fig_eight)
    line_name = []
    for num_line in range(len(subfigure_list)):
        locals()['line_fig_' + str(num_line)] = draw_activation_8.DrawLine(subfigure_list[num_line])
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
    #                           0, actArray_ref[i][4], 0, 0, 0, actArray_ref[i][3], actArray_ref[i][2], 0, actArray_ref[i][1]])
    # else:
    #     muscleActivation = array([0, actArray_ref[i][8], 0, 0, 0, actArray_ref[i][7], actArray_ref[i][6], 0, actArray_ref[i][5],
    #                           0, actArray_ref[i][4], 0, 0, 0, actArray_ref[i][3], actArray_ref[i][2], 0, actArray_ref[i][1]])

    # print(observation)

    # pelvis_height = env.get_state_desc()["body_pos"]["pelvis"][1]
    # print(pelvis_height)
    # pelvis_height = env.get_state_desc()["joint_pos"]["ground_pelvis"]
    # print(pelvis_height)
    # pelvis_tilt = [x*180/3.1415 for x in env.get_state_desc()["joint_pos"]["hip_r"]]

    motionData = motionArray[i]
    targetState = [motionArray[i][4], motionArray[i][7], motionArray[i][8], motionArray[i][9], motionArray[i][12], motionArray[i][13], motionArray[i][3]]
    targetState_balance = motionArray[i][3]

    hip_flexion_r = env.get_state_desc()["joint_pos"]["hip_r"][0] * 180 / 3.1415
    knee_angle_r = env.get_state_desc()["joint_pos"]["knee_r"][0] * 180 / 3.1415
    ankle_angle_r = env.get_state_desc()["joint_pos"]["ankle_r"][0] * 180 / 3.1415
    hip_flexion_l = env.get_state_desc()["joint_pos"]["hip_l"][0] * 180 / 3.1415
    knee_angle_l = env.get_state_desc()["joint_pos"]["knee_l"][0] * 180 / 3.1415
    ankle_angle_l = env.get_state_desc()["joint_pos"]["ankle_l"][0] * 180 / 3.1415
    pelvis_tilt = env.get_state_desc()["joint_pos"]["ground_pelvis"][0] * 180 / 3.1415
    currentState = [hip_flexion_r, knee_angle_r, ankle_angle_r, hip_flexion_l, knee_angle_l, ankle_angle_l, pelvis_tilt]

    PID_out_raw = zeros(6)
    PID_out_new = zeros(6)
    PID_out = zeros(6)
    Error_out = zeros(6)
    sysOut = zeros(6)
    targetState[1] = -50
    # print(currentState[1])
    for PIDnum in range(len(targetState)-1):
        if targetState[PIDnum] <= currentState[PIDnum]:
            PID_out_raw[PIDnum], Error_out[PIDnum] = TestPID.PID_run(WalkPidArray[PIDnum], targetState[PIDnum], currentState[PIDnum])
            PID_out_new[PIDnum] = PID_out_raw[PIDnum] - targetState[PIDnum]
            PID_out[PIDnum] = PID_out_new[PIDnum]
        else:
            PID_out_raw[PIDnum], Error_out[PIDnum] = TestPID.PID_run(WalkPidArray[PIDnum], targetState[PIDnum], currentState[PIDnum])
            PID_out_new[PIDnum] = PID_out_raw[PIDnum] - targetState[PIDnum]
            PID_out[PIDnum] = PID_out_new[PIDnum]
    # PID_out = [xx/500 for xx in PID_out_new]
    print("%9.3f" % PID_out_raw[1], "%9.3f" % Error_out[1], "%9.3f" % PID_out_new[1], "%9.3f" % currentState[1])
    # print(env.get_state_desc()["forces"]["bifemsh_r"])

    act_out = zeros(12)
    for outNum in range(len(PID_out)):
        if PID_out_new[outNum] >= 0:
            act_plus = PID_out[outNum]
            act_minus = 0
            # if act_plus < 0:
            #     act_minus = -act_plus
            #     act_plus = 0
        else:
            act_plus = 0
            act_minus = -PID_out[outNum]
            # if act_minus < 0:
            #     act_plus = - act_minus
            #     act_minus = 0
            # print("***")
        act_out[outNum] = act_plus
        act_out[outNum+6] = act_minus
        if outNum == 1:
            print([act_plus, act_minus])

    # print(act_out[1],  act_out[7])
    # PID_balance_out = -TestPID.PID_run(BalancePid, targetState_balance, pelvis_tilt)/1000
    # if PID_balance_out > 0:
    #     if PID_out[0] > 0 and PID_out[3] < 0:
    #         act_out[3] = PID_balance_out - act_out[0]
    #     elif PID_out[0] < 0 and PID_out[3] > 0:
    #         act_out[0] = PID_balance_out - act_out[3]
    #     elif PID_out[0] > 0 and PID_out[3] > 0:
    #         act_out[0] = act_out[0]*PID_balance_out/(act_out[0]+act_out[3])
    #         act_out[3] = act_out[3]*PID_balance_out/(act_out[0]+act_out[3])
    # else:
    #     if PID_out[0] > 0 and PID_out[3] < 0:
    #         act_out[6] = PID_balance_out - act_out[9]
    #     elif PID_out[0] < 0 and PID_out[3] > 0:
    #         act_out[9] = PID_balance_out - act_out[6]
    #     elif PID_out[0] > 0 and PID_out[3] > 0:
    #         act_out[6] = act_out[6]*PID_balance_out/(act_out[6]+act_out[9])
    #         act_out[9] = act_out[9]*PID_balance_out/(act_out[6]+act_out[9])
    # print("%.3f" % PID_balance_out)
    # print("%.3f" % (-act_out[6]-act_out[9]), "%.3f" % (act_out[0]+act_out[3]))

    # muscleActivation = array([0, act_out[7], act_out[6], act_out[0], 0, act_out[1], act_out[8], 0, act_out[2],
    #                           0, act_out[10], act_out[9], act_out[3], 0, act_out[4], act_out[11], 0, act_out[5]])
    # muscleActivation = array([0, 0, 0, 0, 0, 0, 0, 0, 0,
    #                           0, 0, 0, 0, 0, 0, 0, 0, 0])
    muscleActivation = array([0, act_out[7], 0, 0, 0, 0, 0, 0, 0,
                              0, 0, 0, 0, 0, 0, 0, 0, 0])
    observation, reward, done, info = env.step(muscleActivation)
    current_ = observation
    observation_ = array(current_)
    print(current_)
    # print(pelvis_tilt)

    # print('\n')
    # print(env.get_prev_state_desc()["joint_pos"])
    # print(env.get_observation())
    # print(env.reward())
    if show_fig_one:
        draw_data_one.draw_two(i, currentState[1], targetState[1])
        # print(currentState[1])
        # draw_one_data.draw_one(i, env.get_state_desc()["forces"]["bifemsh_r"])

    if show_fig_eight:
        draw_activation_8.draw_8(i, actArray[i, 1:9], subfigure_list, line_name)




