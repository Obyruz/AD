from Queue import *

class PreemptiveFCFS(Queue):
    
    def __init__(self):
        Queue.__init__(self)
        self.queue1 = []
        self.queue2 = []
    
    def onArrival(self, client):
        print client, "Arrival at", self.time
        if client[CLASS] == 1:
            if self.current[CLASS] == 1:
                self.queue1.append(client)
            else:
                lastClient = (self.current[TIME], self.residual, self.current[CLASS])
                self.queue2.insert(0, lastClient)
                self.residual = client[WORK]
                self.current = client
        else:
            self.queue2.append(client)
            
            
    
    def onService(self):
        if self.queue1:
            next_client = self.queue1.pop(0)
            self.current = next_client
            self.residual = next_client[WORK]
            print "Service Finished at", self.time, "Next", next_client
        elif self.queue2:
            next_client = self.queue2.pop(0)
            self.current = next_client
            self.residual = next_client[WORK]
            print "Service Finished at", self.time, "Next", next_client
        else:
            print "Queue Empty"