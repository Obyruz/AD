from Queue import *

class FCFS(Queue):

    def __init__(self):
        Queue.__init__(self)
        self.queue = []

    def adToQueue(self, client):
        self.queue.append(client)

    def serveNextClient(self):
        if self.queue:
            next_client = self.queue.pop(0)
            self.current = next_client

    def getAllClients(self):
        return self.queue
