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
    return (1/rate)

def unorganizedArrivalWithWork(arrivalRate, workRate, max_time):
    time = nextTime(arrivalRate)
    unorganizedClients = dict()
    while time < max_time:
        work = nextWork(workRate)
        unorganizedClients[time] = work
        time += nextTime(arrivalRate)
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

    for i in range(len(sorted_arrivals)):
        sorted_arrivals[i] = (i,) + sorted_arrivals[i]

    arrivals_file = open("arrivals/arrivals-" + file_name, 'w')
    pickle.dump(sorted_arrivals, arrivals_file, pickle.HIGHEST_PROTOCOL)
    arrivals_file.close()

    # arrivals_file = open("arrivals-"+time.ctime())
    # arrivals_generated = pickle.load(arrivals_file)
    # print arrivals_generated
if __name__ == "__main__":
    main()
