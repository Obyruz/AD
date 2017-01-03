from FCFS import FCFS
from LCFS import LCFS
from PreemptiveLCFS import PreemptiveLCFS
import sys
import pickle

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
        fcfs.clients = pickle.load(file)
        print fcfs.clients
        file.close()
        fcfs.simulate()
        print "Time Average =", fcfs.timeAverage
        print "Work Average =", fcfs.workAverage
        print "Wait Average =", fcfs.waitAverage
        print "Residual Average =", fcfs.residualAverage
    elif queue_type == 'LCFS':
        lcfs = LCFS()
        lcfs.clients = pickle.load(file)
        print lcfs.clients
        file.close()
        lcfs.simulate()
        print "Time Average =", lcfs.timeAverage
        print "Work Average =", lcfs.workAverage
        print "Wait Average =", lcfs.waitAverage
        print "Residual Average =", lcfs.residualAverage
    elif queue_type == 'PreemptiveLCFS':
        preemptivelcfs = PreemptiveLCFS()
        preemptivelcfs.clients = pickle.load(file)
        print preemptivelcfs.clients
        file.close()
        preemptivelcfs.simulate()
        print "Time Average =", preemptivelcfs.timeAverage
        print "Work Average =", preemptivelcfs.workAverage
        print "Wait Average =", preemptivelcfs.waitAverage
        print "Residual Average =", preemptivelcfs.residualAverage

if __name__ == "__main__":
    main()