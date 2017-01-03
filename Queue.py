import abc

TIME = 0
WORK = 1
CLASS = 2

class Queue:
    def __init__(self):
        self.current = None
        self.residual = None
        self.time = 0.0
        self.clients = []
        self.served = []
        
        self.residualTotal = {}
        self.residualClass = {}
        self.timeTotal = {}
        
        self.residualAverage = {}
        self.timeAverage = {}
        self.workAverage = {}
        self.waitAverage = {}
        
    def simulate(self):
        while self.clients or self.current:
            self.nextEvent()
        
        classes = self.timeTotal.keys()
        
        classClients = {}
        
        classClients['all'] = 0
        self.timeTotal['all'] = 0
        self.residualTotal['all'] = 0
        totalWorkAll = 0
        for clazz in classes:
            classClients[clazz] = 0
            for client in self.served:
                if client[CLASS] == clazz:
                    classClients[clazz] += 1
            classClients['all'] += classClients[clazz]
            
            totalWork = 0.0
            for client in self.served:
                if client[CLASS] == clazz:
                    totalWork += client[WORK]
            totalWorkAll += totalWork
                    
            self.workAverage[clazz] = totalWork / classClients[clazz]
            
            self.timeTotal['all'] += self.timeTotal[clazz]
            self.timeAverage[clazz] = self.timeTotal[clazz] / classClients[clazz]
            
            self.waitAverage[clazz] = (self.timeTotal[clazz] - totalWork) / classClients[clazz]
            
            self.residualTotal['all'] += self.residualTotal[clazz]
            if self.residualTotal[clazz]:
                self.residualAverage[clazz] = self.residualTotal[clazz] / classClients[clazz]
            else:
                self.residualAverage[clazz] = 0
        
        self.timeAverage['all'] = self.timeTotal['all'] / classClients['all']
        self.workAverage['all'] = totalWorkAll / classClients['all']
        self.waitAverage['all'] = (self.timeTotal['all'] - totalWorkAll) / classClients['all']
        self.residualAverage['all'] = self.residualTotal['all'] / classClients['all']
    
    def nextEvent(self):
        if self.clients:
            time_until_next_arrival = self.clients[0][TIME] - self.time
            
            if self.current == None:
                self.arrivalEmpty()
            elif time_until_next_arrival < self.residual:
                self.nextArrival()
            else:
                self.nextService()
        elif self.current:
            self.nextService()
    
    def nextArrival(self):
        time_until_next_arrival = self.clients[0][TIME] - self.time
        
        self.time += time_until_next_arrival
        self.residual -= time_until_next_arrival
        
        self.addMetric(self.residualClass, 1, self.current[CLASS])
        self.addMetric(self.residualTotal, self.residual, self.current[CLASS])
        
        client = self.clients.pop(0)
        
        self.onArrival(client)
    
    def nextService(self):
        self.time += self.residual
        
        self.addMetric(self.timeTotal, self.time - self.current[TIME], self.current[CLASS])
        
        self.residual = None
        self.served.append(self.current)
        self.current = None
        
        self.onService()
    
    def arrivalEmpty(self):
        client = self.clients.pop(0)
        self.time = client[TIME]
        
        self.current = client
        self.residual = client[WORK]
        print "Arrival Empty", self.time, client
        
    def addMetric(self, metric, amount, clazz):
        if clazz in metric:
            metric[clazz] += amount
        else:
            metric[clazz] = amount
    
    @abc.abstractmethod
    def onArrival(self, client):
        pass
    
    @abc.abstractmethod
    def onService(self):
        pass
    
    