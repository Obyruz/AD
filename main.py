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

    clientsAverage = {}
    queueClientsAverage = {}
    workAverage = {}
    waitAverage = {}
    timeAverage = {}
    residualAverage = {}
    pendingWorkAverage = {}
    utilisation = {}

    if queue_type == 'FCFS':
        utilisation[1] = float(arrivalValues[LAMBD1]) * float(arrivalValues[MU1])
        utilisation[2] = float(arrivalValues[LAMBD2]) * float(arrivalValues[MU2])
        utilisation['all'] = (utilisation[1] + utilisation[2])
        #clientsAverage['1'] = arrivalValues[LAMBD1]
        #clientsAverage['2'] = arrivalValues[LAMBD2]
        #clientsAverage['all'] = (arrivalValues[LAMBD1] + arrivalValues[LAMBD2])
        #queueClientsAverage['1'] =
        #queueClientsAverage['2'] =
        #queueClientsAverage['all'] =
    print utilisation

def formatArrivalsFile(arrivals_file):
    arrivals = arrivals_file[18:]

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
    print "-----------------------------------"
    print "Clients Average =", queue.clientsAverage
    print "Time Average =", queue.timeAverage
    print "Work Average =", queue.workAverage
    print "Wait Average =", queue.waitAverage
    print "Residual Average =", queue.residualAverage
    print "Pending Work Average =", queue.pendingWorkAverage
    print "Utilisation =", queue.utilisation

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
    run(queue, file)
    generateAnalyticalValues(queue_type, arrivals_file)

if __name__ == "__main__":
    main()
