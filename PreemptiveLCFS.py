from Queue import *
from Client import Client

class PreemptiveLCFS(Queue):
    
    def __init__(self):
        Queue.__init__(self)
        self.queue = []
    
    def adToQueue(self, client):
        lastClient = Client(self.current.id, self.current.time, self.current.residualTime, self.current.clazz)
        self.queue.append(lastClient)
        self.current = client
    
    def serveNextClient(self):
        if self.queue:
            next_client = self.queue.pop(len(self.queue)-1)
            self.current = next_client
            
    def getAllClients(self):
        return self.queue