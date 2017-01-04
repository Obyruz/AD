class Client:
    def __init__(self, id, arrival, work, clazz):
         self.id = id
         self.arrivalTime = arrival
         self.waitTime = 0.0
         self.workTime = 0.0
         self.work = work
         self.clazz = clazz
         
    def residualTime(self):
        return work - workTime