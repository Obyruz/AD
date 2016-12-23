#!/usr/bin/python
# -*- coding: utf-8 -*-
import scipy
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import random
import collections

def nextTime(rate):
    return random.expovariate(rate)

def nextWork(rate):
    return np.random.exponential(rate)

def unorganizedArrivalWithWork(rate, work):
    time = 0
    unorganizedClients = dict()
    while time < 10:
        time += nextTime(rate)
        work = nextWork(rate)
        unorganizedClients[time] = work
    return unorganizedClients

def organizedArrivalWithWork(rate, work):
    clients = collections.OrderedDict(sorted(unorganizedArrivalWithWork(rate, work).items()))
    return clients

def main():
    lambd = 3
    exp = 1

    clientsArrival = organizedArrivalWithWork(lambd, exp)
    print clientsArrival.items()

if __name__ == "__main__":
    main()
