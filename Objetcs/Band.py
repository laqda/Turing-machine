class Band:
    def __init__(self):
        self.list = ['B', 'B', 'B', 'B']
        self.position = 1
        self.state = 1

    def setList(self, give_list=[]):
        self.list = give_list
        return True

    def getList(self):
        return self.list

    def setReadElement(self, give_element):
        self.list[self.position] = give_element
        return True

    def getReadElement(self):
        return self.list[self.position]

    def moveR(self):
        self.position += 1

    def moveL(self):
        self.position -= 1

    def setPosition(self, position):
        self.position = position
        return True

    def getPosition(self):
        return self.position

    def setState(self, state):
        self.state = state
        return True

    def getState(self):
        return self.state