class Client:
    def __init__(self, id, arrival, work, clazz):
         self.id = id
         self.arrivalTime = arrival
         self.waitTime = 0.0
         self.workTime = 0.0
         self.work = work
         self.clazz = clazz
         
    def residualTime(self):
        return self.work - self.workTime
    
    def totalTime(self):
        return self.workTime + self.waitTime
    
    def __str__(self):
        return "({}, {}, {}, {})".format(self.id, self.arrivalTime, self.work, self.clazz)