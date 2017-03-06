import threading


class Parite(threading.Thread):
    def __init__(self, M):
        threading.Thread.__init__(self)
        self.power = True
        self.M = M
        self.B = M.B
        self.state = 1
        self.B.setPosition(1)

    def run(self):
        while self.power:
            self.B.setState(self.state)
            if not self.M.getPause():
                if self.state == 1:
                    self.state1()
                elif self.state == 2:
                    self.state2()
                elif self.state == 3:
                    self.state3()
                elif self.state == 4:
                    self.state4()
                elif self.state == 0:
                    self.finalState()

    def state1(self):
        if self.B.getReadElement() == '0':
            self.B.setReadElement('0')
            self.state = 1
            self.M.wait()
            self.B.moveR()
        elif self.B.getReadElement() == '1':
            self.B.setReadElement('1')
            self.state = 1
            self.M.wait()
            self.B.moveR()
        elif self.B.getReadElement() == 'B':
            self.B.setReadElement('B')
            self.state = 2
            self.M.wait()
            self.B.moveL()

    def state2(self):
        if self.B.getReadElement() == '0':
            self.B.setReadElement('B')
            self.state = 3
            self.M.wait()
            self.B.moveL()
        elif self.B.getReadElement() == '1':
            self.B.setReadElement('B')
            self.state = 4
            self.M.wait()
            self.B.moveL()
        elif self.B.getReadElement() == 'B':
            self.B.setReadElement('B')
            self.state = 2
            self.M.wait()
            self.B.moveL()

    def state3(self):
        if self.B.getReadElement() == '0':
            self.B.setReadElement('B')
            self.state = 3
            self.M.wait()
            self.B.moveL()
        elif self.B.getReadElement() == '1':
            self.B.setReadElement('B')
            self.state = 4
            self.M.wait()
            self.B.moveL()
        elif self.B.getReadElement() == 'B':
            self.B.setReadElement('1')
            self.state = 0
            self.M.wait()
            self.B.moveR()

    def state4(self):
        if self.B.getReadElement() == '0':
            self.B.setReadElement('B')
            self.state = 4
            self.M.wait()
            self.B.moveL()
        elif self.B.getReadElement() == '1':
            self.B.setReadElement('B')
            self.state = 4
            self.M.wait()
            self.B.moveL()
        elif self.B.getReadElement() == 'B':
            self.B.setReadElement('0')
            self.state = 0
            self.M.wait()
            self.B.moveL()

    def finalState(self):
        if self.B.getReadElement() == '1' or self.B.getReadElement() == '0':
            self.M.wait()
            self.B.moveL()
        else:
            self.exit()

    def exit(self):
        self.power = False

    def tableTransition(self):
        e1 = [[0, 0, 'dr', 'e1'], [1, 1, 'dr', 'e1'], ['B', 'B', 'ga', 'e2']]
        e2 = [[0, 'B', 'ga', 'e3'], [1, 'B', 'ga', 'e4'], ['B', 'B', 'ga', 'e2']]
        e3 = [[0, 'B', 'ga', 'e3'], [1, 'B', 'ga', 'e3'], ['B', 1, 'dr', 'ef']]
        e4 = [[0, 'B', 'ga', 'e4'], [1, 'B', 'ga', 'e4'], ['B', 0, 'ga', 'ef']]
        return [e1, e2, e3, e4]
