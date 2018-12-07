from walkingsim import PID
import matplotlib.pyplot as plt

plt.figure(1)
# plt.figure(2)


# Test PID
def TestPID(P, I, D):
    IncrementalPid = PID.IncrementalPID(P, I, D)
    PositionalPid = PID.PositionalPID(P, I, D)
    IncrementalXaxis = [0]
    IncrementalYaxis = [0]
    PositionalXaxis = [0]
    PositionalYaxis = [0]

    for i in range(1, 500):
        # Incremental
        IncrementalPid.SetStepSignal(90)
        IncrementalPid.SetInertiaTime(1, 0.1)
        IncrementalYaxis.append(IncrementalPid.SystemOutput)
        IncrementalXaxis.append(i)

        # Positional
        PositionalPid.SetStepSignal(100.2)
        PositionalPid.SetInertiaTime(3, 0.1)
        PositionalYaxis.append(PositionalPid.SystemOutput)
        PositionalXaxis.append(i)

    plt.figure(1)  # fig 1
    plt.plot(IncrementalXaxis, IncrementalYaxis, 'r')
    plt.xlim(0, 200)
    plt.ylim(0, 200)
    # plt.title("IncrementalPID")

    # plt.figure(2)  # fig 2
    plt.plot(PositionalXaxis, PositionalYaxis, 'b')
    # plt.xlim(0, 120)
    # plt.ylim(0, 140)
    # plt.title("PositionalPID")

    plt.show()


def PID_run(subject, goalState, currentState):
    # IncrementalPid = PID.IncrementalPID(4, 0.5, 0.1)
    PID_out = subject.SetStepSignal(goalState)
    subject.SystemOutput = currentState
    subject.LastSystemOutput = subject.SystemOutput
    # PID.IncrementalYaxis.append(PID.IncrementalPID.SystemOutput)
    # PID.IncrementalXaxis.append(num_step)
    return PID_out


if __name__ == "__main__":
    TestPID(4.5, 0.5, 0.1)



