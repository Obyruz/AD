from Queue import *

class FCFSWithPriority(Queue):
    
    def __init__(self):
        Queue.__init__(self)
        self.queue1 = []
        self.queue2 = []
    
    def adToQueue(self, client):
        if client.clazz == 1:
            self.queue1.append(client)
        else:
            self.queue2.append(client)
    
    def serveNextClient(self):
        if self.queue1:
            next_client = self.queue1.pop(0)
            self.current = next_client
        elif self.queue2:
            next_client = self.queue2.pop(0)
            self.current = next_client
            
    def getAllClients(self):
        return self.queue1 + self.queue2