from random import randrange

from train import Train

class Line:
    def __init__(self, id, name, length, maintenance_exit):
        self.id = id
        self.name = name
        self.length = length
        self.maintenance_check = 8
        self.maintenance_exit = maintenance_exit
        self.trains = []

    def generate_trains(self):
        for i in range(0, randrange(self.length)):
            self.trains.append(Train(i, self.name))