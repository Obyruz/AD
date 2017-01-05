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
    print "Time Average =", queue.timeAverage
    print "Work Average =", queue.workAverage
    print "Wait Average =", queue.waitAverage
    print "Residual Average =", queue.residualAverage
    print "Pending Work Average =", queue.pendingWorkAverage
    print "Utilisation =", queue.utilisation

def main():
    if len(sys.argv) < 3:
        print "ERROR: Less arguments than expected"
        print "python main.py <QUEUE_TYPE> <path_to_arrivals_file>"
        return 
    
    queue_type = sys.argv[1]
    arrivals_file = sys.argv[2]
    
    file = open( arrivals_file )
    
    if queue_type == 'FCFS':
        fcfs = FCFS()
        run(fcfs, file)
        
    elif queue_type == 'LCFS':
        lcfs = LCFS()
        run(lcfs, file)
        
    elif queue_type == 'PreemptiveLCFS':
        preemptivelcfs = PreemptiveLCFS()
        run(preemptivelcfs, file)
        
    elif queue_type == 'PreemptiveFCFS':
    	preemptivefcfs = PreemptiveFCFS()
    	run(preemptivefcfs, file)
    	
    elif queue_type == 'FCFSWithPriority':
    	fcfswithpriority = FCFSWithPriority()
    	run(fcfswithpriority, file)

if __name__ == "__main__":
    main()
