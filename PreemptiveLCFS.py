from Queue import *

class PreemptiveLCFS(Queue):
    
    def __init__(self):
        Queue.__init__(self)
        self.queue = []
    
    def onArrival(self, client):
        print "Arrival at", self.time, client
        lastClient = (self.current[TIME], self.residual, self.current[CLASS])
        self.queue.append(lastClient)
        self.residual = client[WORK]
        self.current = client
    
    def onService(self):
        if self.queue:
            next_client = self.queue.pop(len(self.queue)-1)
            self.current = next_client
            self.residual = next_client[WORK]
            print "Service Finished at", self.time, "Next", next_client
        else:
            print "Queue Empty"