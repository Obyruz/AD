from Queue import *

class LCFS(Queue):
    
    def __init__(self):
        Queue.__init__(self)
        self.queue = []
    
    def onArrival(self, client):
        self.queue.append(client)
    
    def onService(self):
        if self.queue:
            next_client = self.queue.pop(len(self.queue)-1)
            self.current = next_client

    def getAllClients(self):
        return self.queue