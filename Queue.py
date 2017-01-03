import abc

TIME = 0
WORK = 1
CLASS = 2
ARRIVAL = 3

class Queue:
    def __init__(self):
        self.current = None
        self.residual = None
        self.time = 0.0
        self.clients = []
        self.served = []
        
        self.residualTotal = 0.0
        self.timeTotal = 0.0
        
        self.residualAverage = 0.0
        self.timeAverage = 0.0
        self.workAverage = 0.0
        self.waitAverage = 0.0
        
    def simulate(self):
        while self.clients or self.current:
            self.nextEvent()
        
        self.residualAverage = self.residualTotal / len(self.served)
        
        totalWork = 0.0
        for client in self.served:
            totalWork += client[WORK]
        self.workAverage = totalWork / len(self.served)
        
        self.timeAverage = self.timeTotal / len(self.served)
        
        self.waitAverage = (self.timeTotal - totalWork) / len(self.served)
    
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
        
        self.residualTotal += self.residual
        
        client = self.clients.pop(0)
        
        clientWithArrival = (client[TIME], client[WORK], client[CLASS], self.time)
        self.onArrival(clientWithArrival)
    
    def nextService(self):
        self.time += self.residual
        
        self.timeTotal += self.time - self.current[ARRIVAL]
        
        self.residual = None
        self.served.append(self.current)
        self.current = None
        
        self.onService()
    
    def arrivalEmpty(self):
        client = self.clients.pop(0)
        self.time = client[TIME]
        
        clientWithArrival = (client[TIME], client[WORK], client[CLASS], self.time)
        
        self.current = clientWithArrival
        self.residual = clientWithArrival[WORK]
        print "Arrival Empty", self.time
    
    @abc.abstractmethod
    def onArrival(self, client):
        pass
    
    @abc.abstractmethod
    def onService(self):
        pass
    
    