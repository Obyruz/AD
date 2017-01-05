import abc


class Queue:
    def __init__(self):
        self.current = None
        self.time = 0.0
        
        self.clients = []
        self.served = []
        
        self.pendingWorkTotal = 0.0
        self.residualTotal = {}
        self.residualClass = {}
        self.busyTime = {}
        
        self.pendingWorkAverage = 0.0
        self.residualAverage = {}
        self.timeAverage = {}
        self.workAverage = {}
        self.waitAverage = {}
        self.utilisation = {}
        
    def simulate(self):
        while self.clients or self.current:
            self.nextEvent()
        
        classes = self.busyTime.keys()
        
        classClients = {}
        
        classClients['all'] = 0
        self.residualTotal['all'] = 0
        self.residualClass['all'] = 0
        self.busyTime['all'] = 0
        
        timeTotal = {}
        workTotal = {}
        waitTotal = {}
        
        timeTotal['all'] = 0.0
        workTotal['all'] = 0.0
        waitTotal['all'] = 0.0
        
        for clazz in classes:
            classClients[clazz] = 0
            for client in self.served:
                if client.clazz == clazz:
                    classClients[clazz] += 1
            classClients['all'] += classClients[clazz]
            
            timeTotal[clazz] = 0.0
            workTotal[clazz] = 0.0
            waitTotal[clazz] = 0.0
            
            self.utilisation[clazz] = self.busyTime[clazz] / self.time
            self.busyTime['all'] += self.busyTime[clazz]
            
            if clazz in self.residualTotal:
                self.residualAverage[clazz] = self.residualTotal[clazz] / self.residualClass[clazz]
                self.residualTotal['all'] += self.residualTotal[clazz]
                self.residualClass['all'] += self.residualClass[clazz]
            else:
                self.residualAverage[clazz] = 0
        
        for client in self.served:
            timeTotal[client.clazz] += client.totalTime()
            workTotal[client.clazz] += client.workTime
            waitTotal[client.clazz] += client.waitTime
            
            timeTotal['all'] += client.totalTime()
            workTotal['all'] += client.workTime
            waitTotal['all'] += client.waitTime
        
        for clazz in classes + ['all']:
            self.timeAverage[clazz] = timeTotal[clazz] / classClients[clazz]
            self.workAverage[clazz] = workTotal[clazz] / classClients[clazz]
            self.waitAverage[clazz] = waitTotal[clazz] / classClients[clazz]
        
        self.pendingWorkAverage = self.pendingWorkTotal / classClients['all']
        self.residualAverage['all'] = self.residualTotal['all'] / self.residualClass['all']
        self.utilisation['all'] = self.busyTime['all']/self.time
    
    def nextEvent(self):
        if self.clients:
            time_until_next_arrival = self.clients[0].arrivalTime - self.time

            if self.current == None:
                self.arrivalEmpty()
            elif time_until_next_arrival < self.current.residualTime():
                self.nextArrival()
            else:
                self.nextService()
        elif self.current:
            self.nextService()
    
    def nextArrival(self):
        timeUntilNextArrival = self.clients[0].arrivalTime - self.time
        
        self.time += timeUntilNextArrival
        self.addClientTime(timeUntilNextArrival)
        
        self.pendingWorkTotal += self.calculatePendingWork()
        
        self.addMetric(self.residualClass, 1, self.current.clazz)
        self.addMetric(self.residualTotal, self.current.residualTime(), self.current.clazz)
        self.addMetric(self.busyTime, timeUntilNextArrival, self.current.clazz)
        
        client = self.clients.pop(0)
        
        print self.time ,"Arrival:", client
        self.onArrival(client)
    
    def nextService(self):
        residual = self.current.residualTime()
        
        self.time += residual
        self.addClientTime(residual)
        
        self.addMetric(self.busyTime, residual, self.current.clazz)
        served = self.current
        self.served.append(self.current)
        self.current = None
        
        self.onService()
        print self.time, "Served:", served, "/ Next:", (self.current if self.current else "None")
    
    def arrivalEmpty(self):
        client = self.clients.pop(0)
        self.time = client.arrivalTime
        
        self.current = client
        print self.time, "Arrival Empty:", client
        
    def addMetric(self, metric, amount, clazz):
        if clazz in metric:
            metric[clazz] += amount
        else:
            metric[clazz] = amount
    
    def addClientTime(self, timeElapsed):
        for client in self.getAllClients():
            client.waitTime += timeElapsed
        
        self.current.workTime += timeElapsed
    
    def calculatePendingWork(self):
        pendingWork = 0.0
        
        for client in self.getAllClients():
            pendingWork += client.residualTime()
        
        if self.current:
            pendingWork += self.current.residualTime()
        
        return pendingWork

    @abc.abstractmethod    
    def getAllClients(self):
        pass
    
    @abc.abstractmethod
    def onArrival(self, client):
        pass
    
    @abc.abstractmethod
    def onService(self):
        pass
    
    