from Queue import *

class FCFS(Queue):
    
    def __init__(self):
        Queue.__init__(self)
        self.queue = []
    
    def onArrival(self, client):
        print "Arrival", self.time
        self.queue.append(client)
    
    def onService(self):
        print "Service", self.time
        if self.queue:
            next_client = self.queue.pop(0)
            self.current = next_client
            self.residual = next_client[WORK]