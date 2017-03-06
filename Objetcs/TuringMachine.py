import time


class TuringMachine:
    speed = 0.75
    pause = False
    algorithm = 'Incrémentation'
    e1 = [[0, 0, 'dr', 'e1'], [1, 1, 'dr', 'e1'], ['B', 'B', 'ga', 'e2']]
    e2 = [[0, 1, 'ga', 'ef'], [1, 0, 'ga', 'e1'], ['B', 1, 'ga', 'ef']]
    table = [e1, e2]
    A = None
    B = None

    def __init__(self, give_band):
        self.B = give_band

    def wait(self, speed=None):
        if speed is None:
            time.sleep(self.speed)
        else:
            time.sleep(speed)

    def setSpeed(self, give_speed):
        self.speed = give_speed
        return True

    def setAlgorithm(self, give_algorithm):
        self.algorithm = give_algorithm
        return True

    def getSpeed(self):
        return self.speed

    def getAlgorithm(self):
        return self.algorithm

    def setTransitionTable(self, table):
        self.table = table
        return True

    def getTransitionTable(self):
        return self.table

    def setPause(self, give_pause):
        self.pause = give_pause
        return True

    def getPause(self):
        return self.pause