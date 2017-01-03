from FCFS import FCFS
import sys
import pickle

def main():
    if sys.argv[1] == 'FCFS':
        fcfs = FCFS()
        file = open( "arrivals-Tue Jan  3 02:11:43 2017", "r" )
        fcfs.clients = pickle.load(file)
        print fcfs.clients
        file.close()
        fcfs.simulate()
        print "Time Average =", fcfs.timeAverage
        print "Work Average =", fcfs.workAverage
        print "Wait Average =", fcfs.waitAverage
        print "Residual Average =", fcfs.residualAverage

if __name__ == "__main__":
    main()