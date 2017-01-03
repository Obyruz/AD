#!/usr/bin/python
# -*- coding: utf-8 -*-
import numpy as np
import random
import collections
import sys
import pickle
import time

def nextTime(rate):
    return random.expovariate(rate)

def nextWork(rate):
    return np.random.exponential(rate)

def unorganizedArrivalWithWork(rate, work, max_time):
    time = nextTime(rate)
    unorganizedClients = dict()
    while time < max_time:
        work = nextWork(rate)
        unorganizedClients[time] = work
        time += nextTime(rate)
    return unorganizedClients

def organizedArrivalWithWork(rate, work, max_time):
    clients = collections.OrderedDict(sorted(unorganizedArrivalWithWork(rate, work, max_time).items()))
        
    return clients

def main():
    # if len(sys.argv) < 5:
    #     print "Missing parameters" 
    #     print "Expected: python arrivals-generator.py <arrival_rate> <work_rate> <max_time> <number_client_classes>"
    #     return
    
    len_argv = len(sys.argv)
    total_classes = (len_argv - 2)/2
    max_time = int(sys.argv[len_argv-1])
    count = 1
    arrivals = []
    file_name = ""
    
    while count <= total_classes:
        lambd = float(sys.argv[2*count - 1])
        exp = float(sys.argv[2*count])
        file_name += str(lambd) + "_" + str(exp) + "_"
    
        clientsArrival = organizedArrivalWithWork(lambd, exp, max_time)
        
        for key in clientsArrival.keys():
            arrivals.append((key, clientsArrival[key], count))

        count+= 1

    file_name += str(max_time)
    
    sorted_arrivals = sorted(arrivals, key=lambda tup: tup[0])

    arrivals_file = open("arrivals-" + file_name + "-" + time.ctime(), 'w')
    pickle.dump(sorted_arrivals, arrivals_file, pickle.HIGHEST_PROTOCOL)
    arrivals_file.close()
    
    # arrivals_file = open("arrivals-"+time.ctime())
    # arrivals_generated = pickle.load(arrivals_file)
    # print arrivals_generated
if __name__ == "__main__":
    main()