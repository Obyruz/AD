from matplotlib import pyplot as plt
import numpy as np
from main import *
from FCFS import FCFS
import os
import sys

def main():
    if len(sys.argv) < 2:
        print "ERROR: Less arguments than expected"
        print "python main.py <path_to_arrivals_file>"
        return

    folder = sys.argv[1]
    lambda1_lambda2 = []
    pending_work_average_simulated = []
    pending_work_average_analytic = []

    print "ploting files from", folder
    for arrivals in sorted(os.listdir(folder)):
        print "     ", arrivals, "selected"
        arrivals_file = open(folder + arrivals)

        print "     running simulation"
        #print arrivals_file

        fcfs = FCFS()
        simulation_results = run(fcfs, arrivals_file)
        pending_work_average_simulated.append(simulation_results['pending_work_average'])

        print "     calculating analytical values"
        analytical_values = generateAnalyticalValues('FCFS', arrivals)
        params = analytical_values[0]
        analytical_results = analytical_values[1]

        lambda1_lambda2.append(float(params['lambda1'])+float(params['lambda2']))
        pending_work_average_analytic.append(analytical_results['pending_work_average'])

    lambda1_lambda2 = np.array(lambda1_lambda2)
    pending_work_average_simulated = np.array(pending_work_average_simulated)
    pending_work_average_analytic = np.array(pending_work_average_analytic)

    print "     generating plot"
    plt.plot(lambda1_lambda2, pending_work_average_simulated, color='r')
    plt.plot(lambda1_lambda2, pending_work_average_analytic, color='b', linestyle='--')
    plt.savefig('plots/'+folder.split('/')[1]+'.png')
    plt.close()

if __name__ == "__main__":
    main()
