from Queue import *

class FCFSWithPriority(Queue):
    
    def __init__(self):
        Queue.__init__(self)
        self.queue1 = []
        self.queue2 = []
    
    def onArrival(self, client):
        if client[CLASS] == 1:
            self.queue1.append(client)
        else:
            self.queue2.append(client)
            
            
    
    def onService(self):
        if self.queue1:
            next_client = self.queue1.pop(0)
            self.current = next_client
            self.residual = next_client[WORK]
        elif self.queue2:
            next_client = self.queue2.pop(0)
            self.current = next_client
            self.residual = next_client[WORK]