from FCFS import FCFS
from LCFS import LCFS
from PreemptiveLCFS import PreemptiveLCFS
from PreemptiveFCFS import PreemptiveFCFS
from FCFSWithPriority import FCFSWithPriority
from Client import Client
import re
import sys
import pickle

LAMBD1 = 0
LAMBD2 = 2
MU1 = 1
MU2 = 3
TIME = 4

def generateAnalyticalValues(queue_type, arrivals_file):
    arrivalValues = formatArrivalsFile(arrivals_file)

    lambd1 = float(arrivalValues[LAMBD1])
    lambd2 = float(arrivalValues[LAMBD2])
    mu1 = float(arrivalValues[MU1])
    mu2 = float(arrivalValues[MU2])
    lambdTotal = float(arrivalValues[LAMBD1]) + float(arrivalValues[LAMBD2])
    muTotal = (float(arrivalValues[MU1]) + float(arrivalValues[MU2]))/2

    clientsAverage = {}
    queueClientsAverage = {}
    workAverage = {}
    waitAverage = {}
    timeAverage = {}
    residualAverage = {}
    pendingWorkAverage = 0
    utilisation = {}
    busyPeriod = {}

    pendingWorkAverage_q2 = 0
    pendingWorkAverage_q3 = 0
    timeAverage_q4 = {}
    waitAverage_q5 = {}
    time_average_q7 = {}
    waitAverage_q8 = {}
    waitAverage_q9 = {}

    if queue_type == 'FCFS':
        workAverage[1] = (1/mu1)
        workAverage[2] = (1/mu2)
        workAverage['all'] = (1/muTotal)
        utilisation[1] = (lambd1 / mu1)
        utilisation[2] = (lambd1 / mu2)
        utilisation['all'] = lambdTotal / muTotal
        residualAverage[1] = workAverage[1] / 2
        residualAverage[2] = workAverage[2] / 2
        residualAverage['all'] = workAverage['all'] / 2
        pendingWorkAverage = (utilisation['all'] * residualAverage['all'])/(1 - utilisation['all'])
        waitAverage[1] = pendingWorkAverage
        waitAverage[2] = pendingWorkAverage
        waitAverage['all'] = pendingWorkAverage
        queueClientsAverage[1] = lambd1 * waitAverage[1]
        queueClientsAverage[2] = lambd2 * waitAverage[2]
        queueClientsAverage['all'] = lambdTotal * waitAverage['all']
        timeAverage[1] = workAverage[1] + waitAverage[1]
        timeAverage[2] = workAverage[2] + waitAverage[2]
        timeAverage['all'] = workAverage['all'] + waitAverage['all']
        clientsAverage[1] = lambd1 * timeAverage[1]
        clientsAverage[2] = lambd2 * timeAverage[2]
        clientsAverage['all'] = lambdTotal * timeAverage['all']
        busyPeriod['all'] = workAverage['all'] / (1 - utilisation['all'])
    if queue_type == 'LCFS':
        workAverage[1] = (1/mu1)
        workAverage[2] = (1/mu2)
        workAverage['all'] = (1/muTotal)
        utilisation[1] = (lambd1 / mu1)
        utilisation[2] = (lambd1 / mu2)
        utilisation['all'] = lambdTotal / muTotal
        residualAverage[1] = residualAverage[2] = residualAverage['all'] = workAverage['all'] / 2
        pendingWorkAverage = utilisation['all'] * residualAverage['all']/(1 - utilisation['all'])
        waitAverage[1] = pendingWorkAverage
        waitAverage[2] = pendingWorkAverage
        waitAverage['all'] = pendingWorkAverage
        timeAverage[1] = waitAverage[1] + workAverage[1]
        timeAverage[2] = waitAverage[2] + workAverage[2]
        timeAverage['all'] = waitAverage['all'] + workAverage['all']
        queueClientsAverage[1] = lambd1 * waitAverage[1]
        queueClientsAverage[2] = lambd2 * waitAverage[2]
        queueClientsAverage['all'] = lambdTotal * waitAverage['all']
        clientsAverage[1] = lambd1 * timeAverage[1]
        clientsAverage[2] = lambd2 * timeAverage[2]
        clientsAverage['all'] = lambdTotal * timeAverage['all']
        busyPeriod['all'] = workAverage['all'] / (1 - utilisation['all'])
    if queue_type == 'PreemptiveLCFS':
        workAverage[1] = (1/mu1)
        workAverage[2] = (1/mu2)
        workAverage['all'] = (1/muTotal)
        utilisation[1] = (lambd1 / mu1)
        utilisation[2] = (lambd1 / mu2)
        utilisation['all'] = lambdTotal / muTotal
        residualAverage[1] = residualAverage[2] = residualAverage['all'] = workAverage['all'] / 2
        pendingWorkAverage = utilisation['all'] * residualAverage['all'] / (1 - utilisation['all'])
        timeAverage[1] = workAverage[1] / (1 - (utilisation[1] + utilisation[2]))
        timeAverage[2] = workAverage[2] / (1 - (utilisation[1] + utilisation[2]))
        timeAverage['all'] = workAverage['all'] / (1 - utilisation['all'])
        clientsAverage[1] = lambd1 * timeAverage[1]
        clientsAverage[2] = lambd2 * timeAverage[2]
        clientsAverage['all'] = lambdTotal * timeAverage['all']
        waitAverage[1] = (utilisation[1] * workAverage[1] + utilisation[2] * workAverage[2]) / (1 - utilisation['all'])
        waitAverage[2] = (utilisation[2] * workAverage[2] + utilisation[1] * workAverage[1]) / (1 - utilisation['all'])
        waitAverage['all'] = utilisation['all'] * workAverage['all'] / (1 - utilisation['all'])
        queueClientsAverage[1] = lambd1 * waitAverage[1]
        queueClientsAverage[2] = lambd2 * waitAverage[2]
        queueClientsAverage['all'] = lambdTotal * waitAverage['all']
        busyPeriod['all'] = workAverage['all'] / (1 - utilisation['all'])
    if queue_type == 'FCFSWithPriority':
        workAverage[1] = (1/mu1)
        workAverage[2] = (1/mu2)
        workAverage['all'] = workAverage[1] * (lambd1/lambdTotal) + workAverage[2] * (lambd2/lambdTotal)
        utilisation[1] = (lambd1 / mu1)
        utilisation[2] = (lambd2 / mu2)
        utilisation['all'] = utilisation[1] + utilisation[2]
        residualAverage[1] = residualAverage[2] = residualAverage['all'] = workAverage['all'] / 2
        pendingWorkAverage = utilisation['all'] * residualAverage['all']/(1 - utilisation['all'])
        waitAverage[1] = residualAverage['all'] / (1 - utilisation[1])
        waitAverage[2] = residualAverage['all'] / (1 - (utilisation[1] + utilisation[2]))
        waitAverage['all'] = waitAverage[1] * (utilisation[1]/(utilisation[1]+utilisation[2])) + waitAverage[2] * (utilisation[2]/(utilisation[1]+utilisation[2]))
        queueClientsAverage[1] = lambd1 * waitAverage[1]
        queueClientsAverage[2] = lambd2 * waitAverage[2]
        queueClientsAverage['all'] = queueClientsAverage[1] + queueClientsAverage[2]
        timeAverage[1] = workAverage[1] + waitAverage[1]
        timeAverage[2] = workAverage[2] + waitAverage[2]
        timeAverage['all'] = workAverage['all'] + waitAverage['all']
        clientsAverage[1] = lambd1 * timeAverage[1]
        clientsAverage[2] = lambd2 * timeAverage[2]
        clientsAverage['all'] = clientsAverage[1] + clientsAverage[2]
        busyPeriod['all'] = workAverage['all'] / (1 - utilisation['all'])
    if queue_type == 'PreemptiveFCFS':
        workAverage[1] = (1/mu1)
        workAverage[2] = (1/mu2)
        workAverage['all'] = workAverage[1] * (lambd1/lambdTotal) + workAverage[2] * (lambd2/lambdTotal)
        utilisation[1] = lambd1*workAverage[1]
        utilisation[2] = lambd2*workAverage[2]
        utilisation['all'] = utilisation[1] + utilisation[2]
        residualAverage[1] = residualAverage[2] = residualAverage['all'] =  workAverage[1] / 2
        pendingWorkAverage = utilisation['all'] * residualAverage['all']/(1 - utilisation['all'])
        waitAverage[1] = utilisation[1] * residualAverage[1] / (1 - utilisation[1])
        waitAverage[2] = (utilisation[1] * residualAverage[1] + utilisation[2] * residualAverage[2] + utilisation[1] * workAverage[1]) / (1 - utilisation['all'])
        waitAverage['all'] = waitAverage[1] * (utilisation[1]/(utilisation[1]+utilisation[2])) + waitAverage[2] * (utilisation[2]/(utilisation[1]+utilisation[2]))
        queueClientsAverage[1] = lambd1 * waitAverage[1]
        queueClientsAverage[2] = lambd2 * waitAverage[2]
        queueClientsAverage['all'] = queueClientsAverage[1] + queueClientsAverage[2]
        timeAverage[1] = workAverage[1] + waitAverage[1]
        timeAverage[2] = workAverage[2] + waitAverage[2]
        timeAverage['all'] = workAverage['all'] + waitAverage['all']
        clientsAverage[1] = lambd1 * timeAverage[1]
        clientsAverage[2] = lambd2 * timeAverage[2]
        clientsAverage['all'] = clientsAverage[1] + clientsAverage[2]
        busyPeriod['all'] = workAverage['all'] / (1 - utilisation['all'])

    pendingWorkAverage_q2 = (residualAverage[1]*utilisation[1] + residualAverage[2]*utilisation[2] + utilisation['all']*residualAverage['all'])/(1 - utilisation['all'])
    pendingWorkAverage_q3 = queueClientsAverage[1]* workAverage[1] +  queueClientsAverage[2]* workAverage[2] + workAverage[1]*utilisation[1] + workAverage[2]*utilisation[2]
    timeAverage_q4[2] = (workAverage[2] + pendingWorkAverage)/(1 - utilisation[1])
    waitAverage_q5[2] = pendingWorkAverage/(1 - utilisation[1])
    time_average_q7['all'] = workAverage['all']/ (1 - utilisation['all'])
    waitAverage_q8[1] = workAverage[1]/(1 - utilisation[1])
    waitAverage_q9[1] = (utilisation[1]*residualAverage[1])/(1-utilisation[1])

    params = {'lambda1' : arrivalValues[LAMBD1], 'lambda2' : arrivalValues[LAMBD2]}
    analytical_results = {'clientsAverage' : clientsAverage, 'queue_clients_average' : queueClientsAverage, 'time_average' : timeAverage, 'time_average_q4' : timeAverage_q4, 'time_average_q7' : time_average_q7, 'work_average' : workAverage, 'wait_average' :  waitAverage, 'wait_average_q5' :  waitAverage_q5, 'wait_average_q8' :  waitAverage_q8, 'wait_average_q9' :  waitAverage_q9, 'residual_average' : residualAverage, 'pending_work_average' : pendingWorkAverage, 'pending_work_average_q2' : pendingWorkAverage_q2, 'pending_work_average_q3' : pendingWorkAverage_q3, 'utilisation' : utilisation, 'busyPeriod' : busyPeriod}

    return (params, analytical_results)


def formatArrivalsFile(arrivals_file):
    hyphen_pos = arrivals_file.index('-')
    arrivals = arrivals_file[hyphen_pos+1:]

    count = 1
    arrivalValues = list()
    while "_" in arrivals:
        if count == 1:
            parameterStart = 0
        else:
            parameterStart = parameterEnd
        parameterEnd = re.search(r"\_", arrivals).start()

        if (count % 4) == 1:
            lambd1 = arrivals[0:parameterEnd]
            arrivalValues.append(lambd1)
        elif (count % 4) == 2:
            mu1 = arrivals[0:parameterEnd]
            arrivalValues.append(mu1)
        elif (count % 4) == 3:
            lambd2 = arrivals[0:parameterEnd]
            arrivalValues.append(lambd2)
        else:
            mu2 = arrivals[0:parameterEnd]
            arrivalValues.append(mu2)
        arrivals = arrivals[parameterEnd+1:]
        count += 1
    totalTime = arrivals
    arrivalValues.append(totalTime)

    return arrivalValues

def run(queue, file):
    clientsBuffer = pickle.load(file)

    for clt in clientsBuffer:
        client = Client(clt[0], clt[1], clt[2], clt[3])
        queue.clients.append(client)

    # print queue.clients
    file.close()
    queue.simulate()
    queue.calculateMetrics()

    simulated_results = {'clients_average' : queue.clientsAverage, 'time_average' : queue.timeAverage, 'work_average' : queue.workAverage, 'wait_average' : queue.waitAverage, 'residual_Average' : queue.residualAverage, 'pending_work_average' : queue.pendingWorkAverage, 'utilisation' : queue.utilisation}
    return simulated_results

def main():
    verbose = False
    i = 0
    while i < len(sys.argv):
        if sys.argv[i] == '-v':
            verbose = True
            del sys.argv[i]
        else:
            i += 1

    if len(sys.argv) < 3:
        print "ERROR: Less arguments than expected"
        print "python main.py <QUEUE_TYPE> <path_to_arrivals_file> [-v]"
        return

    queue_type = sys.argv[1]
    arrivals_file = sys.argv[2]

    file = open( arrivals_file )

    if queue_type == 'FCFS':
        queue = FCFS()
    elif queue_type == 'LCFS':
        queue = LCFS()
    elif queue_type == 'PreemptiveLCFS':
        queue = PreemptiveLCFS()
    elif queue_type == 'PreemptiveFCFS':
    	queue = PreemptiveFCFS()
    elif queue_type == 'FCFSWithPriority':
    	queue = FCFSWithPriority()
    else:
        print "Queue type not supported. Please choose one of the following:"
        print "FCFS"
        print "LCFS"
        print "PreemptiveLCFS"
        print "PreemptiveFCFS"
        print "FCFSWithPriority"
        return

    queue.verbose = verbose
    print run(queue, file)
    print generateAnalyticalValues(queue_type, arrivals_file)

if __name__ == "__main__":
    main()
