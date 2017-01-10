from FCFS import FCFS
from LCFS import LCFS
from PreemptiveLCFS import PreemptiveLCFS
from PreemptiveFCFS import PreemptiveFCFS
from FCFSWithPriority import FCFSWithPriority
from Client import Client
import sys
import pickle

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

if __name__ == "__main__":
    main()
