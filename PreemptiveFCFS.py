from Queue import *
from Client import Client

class PreemptiveFCFS(Queue):
    
    def __init__(self):
        Queue.__init__(self)
        self.queue1 = []
        self.queue2 = []
    
    def onArrival(self, client):
        if client.clazz == 1:
            if self.current.clazz == 1:
                self.queue1.append(client)
            else:
                lastClient = Client(self.current.id, self.current.time, self.current.residualTime, self.current.clazz)
                self.queue2.insert(0, lastClient)
                self.current = client
        else:
            self.queue2.append(client)

    
    def onService(self):
        if self.queue1:
            next_client = self.queue1.pop(0)
            self.current = next_client
        elif self.queue2:
            next_client = self.queue2.pop(0)
            self.current = next_client
            
    def getAllClients(self):
        return self.queue1 + self.queue2