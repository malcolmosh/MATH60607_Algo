import random
class Optimization_random:
    def __init__(self, data):
        self.data = data
    def optimize(self, rate_use=50):
        if (type(rate_use) is not int): rate_use=50
        elif rate_use < 0: rate_use = 0
        elif rate_use > 100: rate_use = 100
        #Comprehension list to choose a bool value for each chair | The [0] is because the random.choices return a list of k element (by defaut k=1)
        self.data = [[chair[0],chair[1],chair[2],random.choices([True, False],[rate_use, 100 - rate_use])[0]] for chair in self.data]
        return self.data
