import threading


class Doubler(threading.Thread):
    def __init__(self, M):
        threading.Thread.__init__(self)
        self.power = True
        self.M = M
        self.B = M.B
        self.state = 1
        self.B.setPosition(1)

    def run(self):
        liste = self.B.getList()
        for i in range(1, len(liste) - 1):
            if liste[i] != '1':
                self.power = False
                print("Entrer un entier valide")
                break

        while self.power:
            if not self.M.getPause():
                self.B.setState(self.state)
                if self.state == 1:
                    self.state1()
                elif self.state == 2:
                    self.state2()
                elif self.state == 3:
                    self.state3()
                elif self.state == 0:
                    self.finalState()

    def state1(self):
        if self.B.getReadElement() == '0':
            self.B.setReadElement('0')
            self.state = 1
            self.M.wait()
            self.B.moveR()
        elif self.B.getReadElement() == '1':
            self.B.setReadElement('0')
            self.state = 2
            self.M.wait()
            self.B.moveL()
        elif self.B.getReadElement() == 'B':
            self.B.setReadElement('B')
            self.state = 3
            self.M.wait()
            self.B.moveL()

    def state2(self):
        if self.B.getReadElement() == '0':

            self.B.setReadElement('0')
            self.state = 2
            self.M.wait()
            self.B.moveL()
        elif self.B.getReadElement() == 'B':
            liste = self.B.getList()
            liste.insert(1, '0')
            self.B.setList(liste)
            self.state = 1
            self.M.wait()
            self.B.moveR()

    def state3(self):
        if self.B.getReadElement() == '0':
            self.B.setReadElement('1')
            self.state = 3
            self.M.wait()
            self.B.moveL()
        elif self.B.getReadElement() == 'B':
            self.B.setReadElement('B')
            self.state = 0
            self.M.wait()
            self.B.moveR()

    def finalState(self):
        if self.B.getReadElement() == '1' or self.B.getReadElement() == '0':
            self.M.wait()
            self.B.moveL()
        else:
            self.exit()

    def exit(self):
        self.power = False

    def tableTransition(self):
        e1 = [[0, 0, 'dr', 'e1'], [1, 0, 'ga', 'e2'], ['B', 'B', 'ga', 'e3']]
        e2 = [[0, 0, 'ga', 'e2'], [1, 1, 'ga', 'e2'], ['B', 0, 'dr', 'e1']]
        e3 = [[0, 1, 'ga', 'e3'], [1, 1, 'ga', 'e3'], ['B', 'B', 'ga', 'ef']]
        return [e1, e2, e3]
