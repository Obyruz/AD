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
        
    def simulate(self):
        while self.clients or self.current:
            self.nextEvent()
    
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
        
        client = self.clients.pop(0)
        self.onArrival(client)
    
    def nextService(self):
        self.time += self.residual
        self.residual = None
        self.served.append(self.current)
        self.current = None
        
        self.onService()
    
    def arrivalEmpty(self):
        client = self.clients.pop(0)
        self.time = client[TIME]
        self.current = client
        self.residual = client[WORK]
        print "Arrival Empty", self.time
    
    @abc.abstractmethod
    def onArrival(self, client):
        pass
    
    @abc.abstractmethod
    def onService(self):
        pass
    
    