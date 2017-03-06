import display
from Objetcs import TuringMachine
from Objetcs import Band

B = Band.Band()
M = TuringMachine.TuringMachine(B)

if __name__ == "__main__":
    display.TuringDisplay(M).mainloop()
