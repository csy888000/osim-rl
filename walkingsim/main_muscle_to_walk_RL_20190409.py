from osim.env import OneJoint

import numpy as np
from walkingsim import readExcel, draw_data_one, draw_activation_8, PID, TestPID, RL_brain, draw_fig
import matplotlib.pyplot as plt

# from RL_brain import DeepQNetwork

# Read muscle activation data
roundNum = 1
actList, actArray_ref = readExcel.excel_table_byindex(startRow=23)

motionList, motionArray_raw = readExcel.excel_table_byindex_raw(startRow=0, file='normal_new.xls', colnameindex=0, by_index=0)
motionArray = np.tile(motionArray_raw, (roundNum, 1))

print(actArray_ref.shape)
print(motionArray.shape)
# for row in motionList:
#     print(row)

# print(tableMatrix)
# print(len(tableList))


# get simulation environment
# show opensim model?
env = OneJoint(visualize=True)
env.list_elements()

istepMax = 0
total_steps = 0
target_one = -30

# numStep = 201 * roundNum

'''
for subNum in range(6):
    locals()['WalkPid' + str(subNum)] = PID.PositionalPID(5, 0, 1)  # (45, 0.7, 580) (20, 0.5, 100)
for subNum2 in range(6):
    locals()['WalkPid' + str(subNum2+6)] = PID.PositionalPID(20, 0.5, 100)  # (10, 0.8, 10)
WalkPidArray = [WalkPid0, WalkPid1, WalkPid2, WalkPid3, WalkPid4, WalkPid5]
WalkPidBackArray = [WalkPid6, WalkPid7, WalkPid8, WalkPid9, WalkPid10, WalkPid11]
BalancePid = PID.IncrementalPID(15, 0.5, 0.1)
IncrementalXaxis = [0]
IncrementalYaxis = [0]
'''
# draw_8 a specific data

# show figures?
show_fig_one = True
show_fig_eight = False
TwoFig = draw_fig.DrawTwo(show_fig_one)
fig_handle_two = draw_fig.DrawTwo.set_fig_2(TwoFig)

# draw_8 muscle activations
EightFig = draw_fig.DrawEight(show_fig_eight)
fig_handle_eight = draw_fig.DrawEight.set_figure_8(EightFig)


RL = RL_brain.DeepQNetwork(n_actions=2,
                      n_features=14,
                      learning_rate=0.01, e_greedy=0.9,
                      replace_target_iter=100, memory_size=2000,
                      e_greedy_increment=0.0008,)

for i_episode in range(100):

    observation = env.reset()
    ep_r = 0
    iStep = 0
    currentState = env.get_observation()
    observation = np.array([i * 180 / 3.1415 for i in currentState])

    while True:

        # muscleActivation = env.action_space.sample()
        # MH(knee flexor/hip extensor), VL (hip flexor/knee extensor)
        # MG (knee flexor/ankle plantarflexor, TA (the main ankle dorsiflexor)
        # muscleActivation = array([i/numStep, 0, 0, 0.7, 0, 0, 0, 0, 0, i/numStep, 0, 0, 0.7, 0, 0, 0, 0, 0])
        #right\left

        '''
        motionData = motionArray[i]
        # hip_flexion_r, knee_angle_r, ankle_angle_r, hip_flexion_l, knee_angle_l, ankle_angle_l, pelvis_tilt
        targetState = [motionArray[i][4], motionArray[i][7], motionArray[i][8], motionArray[i][9], motionArray[i][12], motionArray[i][13], motionArray[i][3]]
        # pelvis_tilt
        targetState_balance = motionArray[i][3]
        '''

        # print(env.get_state_desc())
        # hip_flexion_r = env.get_state_desc()["joint_pos"]["hip_r"][0] * 180 / 3.1415
        # knee_angle_r = env.get_state_desc()["joint_pos"]["knee_r"][0] * 180 / 3.1415
        # ankle_angle_r = env.get_state_desc()["joint_pos"]["ankle_r"][0] * 180 / 3.1415
        # hip_flexion_l = env.get_state_desc()["joint_pos"]["hip_l"][0] * 180 / 3.1415
        # knee_angle_l = env.get_state_desc()["joint_pos"]["knee_l"][0] * 180 / 3.1415
        # ankle_angle_l = env.get_state_desc()["joint_pos"]["ankle_l"][0] * 180 / 3.1415
        # pelvis_tilt = env.get_state_desc()["joint_pos"]["ground_pelvis"][0] * 180 / 3.1415
        # currentState = [hip_flexion_r, knee_angle_r, ankle_angle_r, hip_flexion_l, knee_angle_l, ankle_angle_l, pelvis_tilt]
        # observation = array(currentState)
        # print('obs = ', observation)

        act_out = np.zeros(2)
        action = RL.choose_action(observation)
        # print('action = ', action)
        # if action >= 0:
        #     act_out[0] = action
        # else:
        #     act_out[1] = -action
        #     print(act_out[1])
        muscleActivation = np.array([0, action*0.9, 0, 0, 0, 0, 0, 0, 0,
                                    0, 0, 0, 0, 0, 0, 0, 0, 0])
        # current muscle activation for synergy
        actArray_obs = muscleActivation[[17, 15, 14, 10, 8, 6, 5, 1]]

        # print('act = ', actArray_obs)
        currentState_, reward, done, info = env.step(muscleActivation)
        # print(done)
        observation_ = np.array([i * 180 / 3.1415 for i in currentState_])
        # print(np.round(observation_, 2))
        r1th = 5
        r2th = 5
        r1 = (r1th - abs(target_one - observation_[1]))/r1th
        r2 = (r2th-abs(observation_[8]))/r2th
        r3 = -env.istep/10
        reward = r1
        # print(r1, r2)
        # print('env.istep = ', env.istep)
        # print('istep =', istep)
        # print('pos=', abs(target_one - observation_[1]), 'vel=', abs(observation_[8]), 'reward=', reward)
        # print(reward)
        # print(pelvis_tilt)

        # print('\n')
        # print(env.get_prev_state_desc()["joint_pos"])
        # print(env.get_observation())
        # print(env.reward())

        # 保存这一组记忆
        RL.store_transition(observation, action, reward, observation_)

        if total_steps > 1000:
            RL.learn()  # 学习
            # print('Learned')

        ep_r += reward
        # i_episode = 1
        if done:
            print('episode: ', i_episode,
                  'ep_r: ', round(ep_r, 2),
                  'epsilon: ', round(RL.epsilon, 2),
                  'total_steps:', total_steps)
            break

        if iStep > istepMax:
            istepMax = iStep

        if show_fig_one:
            draw_fig.DrawTwo.draw_two(TwoFig, iStep, observation_[1], target_one, istepMax)
        plt.savefig('Real-TimeData.png')

        if show_fig_eight:
            draw_fig.DrawEight.draw_8(EightFig, iStep, actArray_ref[iStep, 1:9], EightFig.subfigure_list)

        observation = observation_
        total_steps += 1
        iStep += 1
    # draw_fig.DrawEight.clear_fig(EightFig)
        # plt.savefig('Real-TimeData.png')


print('step = ', total_steps)
RL.plot_cost()

