from matplotlib import pyplot as plt
import numpy as np
from main import *
import os
import sys

def main():
    if len(sys.argv) < 2:
        print "ERROR: Less arguments than expected"
        print "python main.py <path_to_arrivals_file>"
        return

    folder = sys.argv[1]
    #fcfs = FCFS()
    queue = "preemptive"

    for i in range(1,10):
        lambda1_lambda2 = []
        simulated = []
        simulated2 = []
        analytic = []

        print "QUESTAO", i

        print "ploting files from", folder

        for arrivals in sorted(os.listdir(folder)):
            print "     ", arrivals, "selected"
            arrivals_file = open(folder + arrivals)

            preemptive = PreemptiveFCFS()

            print "     running simulation"
            simulation_results = run(preemptive, arrivals_file)

            print "     calculating analytical values"
            analytical_values = generateAnalyticalValues('PreemptiveFCFS', arrivals)

            params = analytical_values[0]
            analytical_results = analytical_values[1]

            if (i == 1):
                plt.ylabel('Pending Work Average')
                simulated.append(simulation_results['pending_work_average'])
                analytic.append(analytical_results['pending_work_average'])

            elif (i == 2):

                plt.ylabel('Pending Work Average')
                simulated.append(simulation_results['pending_work_average'])
                analytic.append(analytical_results['pending_work_average_q2'])


            elif (i == 3):
                plt.ylabel('Pending Work Average')
                simulated.append(simulation_results['pending_work_average'])
                analytic.append(analytical_results['pending_work_average_q3'])

            elif (i == 4):
                plt.ylabel('Time Average Client 2')
                simulated.append(simulation_results['time_average'][2])
                analytic.append(analytical_results['time_average_q4'][2])

            elif (i == 5):
                plt.ylabel('Wait Average Client 2')
                simulated.append(simulation_results['wait_average'][2])
                analytic.append(analytical_results['wait_average_q5'][2])

            elif (i == 6):
                simulated.append(simulation_results['wait_average'][1])
                simulated2.append(simulation_results['wait_average'][2])

                analytic.append(analytical_results['pending_work_average'])

            elif (i == 7):
                plt.ylabel('Time Average')
                simulated.append(simulation_results['time_average']['all'])
                analytic.append(analytical_results['time_average_q7']['all'])
            elif (i == 8):
                plt.ylabel('Wait Average Client 1')
                simulated.append(simulation_results['wait_average'][1])
                analytic.append(analytical_results['wait_average_q8'][1])
            elif (i == 9):
                plt.ylabel('Wait Average Client 1')
                simulated.append(simulation_results['wait_average'][1])
                analytic.append(analytical_results['wait_average_q9'][1])
            elif (i == 10):
                pass

            lambda1_lambda2.append(float(params['lambda1'])+float(params['lambda2']))

        lambda1_lambda2 = np.array(lambda1_lambda2)
        simulated = np.array(simulated)
        analytic = np.array(analytic)
        simulated2 = np.array(simulated2)

        print "     generating plot"

        if i != 6:
            plt.plot(lambda1_lambda2, simulated, color='r')
            plt.plot(lambda1_lambda2, analytic, color='b', linestyle='--')

        else:
            f, axis = plt.subplots(2, sharex=True)

            axis[0].plot(lambda1_lambda2, simulated, color='r')
            axis[0].plot(lambda1_lambda2, analytic, color='b', linestyle='--')
            axis[0].set_xlabel(r'$\lambda$')
            axis[0].set_ylabel('Wait Average Client 1')
            axis[1].plot(lambda1_lambda2, simulated2, color='r')
            axis[1].plot(lambda1_lambda2, analytic, color='b', linestyle='--')
            axis[1].set_xlabel(r'$\lambda$')
            axis[1].set_ylabel('Wait Average Client 2')

        plt.savefig('plots/' + str(i) + '-' + queue + '-' + folder.split('/')[1]+'.png')
        plt.close()

if __name__ == "__main__":
    main()
