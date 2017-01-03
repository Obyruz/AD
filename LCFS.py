from Queue import *

class LCFS(Queue):
    
    def __init__(self):
        Queue.__init__(self)
        self.queue = []
    
    def onArrival(self, client):
        print "Arrival", self.time, client
        self.queue.append(client)
    
    def onService(self):
        if self.queue:
            next_client = self.queue.pop(len(self.queue)-1)
            self.current = next_client
            self.residual = next_client[WORK]
            print "Service", self.time, next_client
        else:
            print "Queue Empty"