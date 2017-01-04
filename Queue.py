import abc

ID   = 0
TIME = 1
WORK = 2
CLASS = 3

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
        self.workTotal = {}
        
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
        self.workTotal['all'] = 0
        self.residualTotal['all'] = 0
       
        for clazz in classes:
            classClients[clazz] = 0
            for client in self.served:
                if client[CLASS] == clazz:
                    classClients[clazz] += 1
            classClients['all'] += classClients[clazz]
            
            self.workAverage[clazz] = self.workTotal[clazz] / classClients[clazz]
            self.timeAverage[clazz] = self.timeTotal[clazz] / classClients[clazz]
            self.waitAverage[clazz] = (self.timeTotal[clazz] - self.workTotal[clazz]) / classClients[clazz]
            
            self.workTotal['all'] += self.workTotal[clazz]
            self.timeTotal['all'] += self.timeTotal[clazz]
            self.residualTotal['all'] += self.residualTotal[clazz]
            
            if self.residualTotal[clazz]:
                self.residualAverage[clazz] = self.residualTotal[clazz] / classClients[clazz]
            else:
                self.residualAverage[clazz] = 0
        
        self.timeAverage['all'] = self.timeTotal['all'] / classClients['all']
        self.workAverage['all'] = self.workTotal['all'] / classClients['all']
        self.waitAverage['all'] = (self.timeTotal['all'] - self.workTotal['all']) / classClients['all']
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
        
        self.addMetric(self.workTotal, client[WORK], client[CLASS])
        
        print self.time ,"Arrival:", client
        self.onArrival(client)
    
    def nextService(self):
        self.time += self.residual
        
        self.addMetric(self.timeTotal, self.time - self.current[TIME], self.current[CLASS])
        served = self.current
        self.residual = None
        self.served.append(self.current)
        self.current = None
        
        self.onService()
        print self.time, "Served:", served, "/ Next:", (self.current if self.current else "None")
    
    def arrivalEmpty(self):
        client = self.clients.pop(0)
        self.time = client[TIME]
        
        self.current = client
        self.residual = client[WORK]
        print self.time, "Arrival Empty:", client
        
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
    
    