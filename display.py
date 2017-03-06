from Algorithms import Incrementation
from Algorithms import Decrementation
from Algorithms import Inverser
from Algorithms import Parite
from Algorithms import Multiplication
from Algorithms import Doubler
from tkinter import *
import time


class TableDeTransition(LabelFrame):
    def __init__(self, boss):
        LabelFrame.__init__(self, boss=None)
        self.configure(text="Table de Transition", font=('Times', 12), borderwidth=3)

        self.boss = boss
        self.table = []
        self.liste = ["Lit", "Ecrit", "Dep", "Etat"]
        self.nbEtats = len(self.table)
        self.canvas = Canvas(self, width=201, height=90 * self.nbEtats + 31)

    def tracer(self):
        self.table = self.boss.M.getTransitionTable()
        self.nbEtats = len(self.table)
        self.canvas.configure(height=90 * self.nbEtats + 31)
        self.canvas.delete(ALL)

        for y in range(self.nbEtats):
            Y = 90 * y + 31
            self.canvas.create_text(24, 15 + Y, text="e{}".format(y + 1), font=('Times', 12))
            for x in range(5):
                X = 40 * x + 2
                if x > 0:
                    self.canvas.create_rectangle(X, 2, X + 40, 31)
                    self.canvas.create_text(X + 20, 17, text=self.liste[x - 1], font=('Times', 10))
                for k in range(3):
                    if x > 0:
                        self.canvas.create_text(X + 20, Y + 30 * k + 15, text=self.table[y][k][x - 1],
                                                font=('Times', 12))
                    if x == 0:
                        if k == 0:
                            self.canvas.create_rectangle(X, Y + 30 * k, X + 40, Y + 90 * (1 + k))
                    else:
                        self.canvas.create_rectangle(X, Y + 30 * k, X + 40, Y + 30 * (1 + k))
        self.canvas.grid(padx=5, pady=5)
        self.boss.update()


class ChoixAlgo(Listbox):
    def __init__(self, boss):
        self.boss = boss
        Listbox.__init__(self, boss=None, height=7, width=500, font=('Times', 11))
        self.config(bg='grey90', width=25)
        self.insert(END, "  Incrémentation")
        self.insert(END, "  Décrémentation")
        self.insert(END, "  Addition")
        self.insert(END, "  Multiplication par 2")
        self.insert(END, "  Tester la parité")
        self.insert(END, "  Inverser les 0 et les 1")
        self.insert(END, "  Doubler une liste de 1")

        self.bind('<ButtonRelease-1>', self.list_box)

    def list_box(self, evt):
        i = self.curselection()
        if not self.boss.A is None:
            if not self.boss.A.isAlive():
                self.boss.M.setAlgorithm(self.get(i)[2:])
                self.boss.selectAlgo()
        else:
            self.boss.M.setAlgorithm(self.get(i)[2:])
            self.boss.selectAlgo()


class BandDisplay(Canvas):
    def __init__(self, boss):
        Canvas.__init__(self, boss=None)

        self.configure(width=871, height=65)
        self.boss = boss
        self.liste = self.boss.M.B.getList()
        self.position = self.boss.M.B.getPosition()
        self.state = self.boss.M.B.getState()

    def tracer(self):
        self.delete(ALL)
        self.liste = self.boss.M.B.getList()
        self.position = self.boss.M.B.getPosition()
        self.state = self.boss.M.B.getState()
        if self.state == 0: self.state = 'f'
        self.state = "etat " + str(self.state)
        self.create_text(380, 18, text=self.state, font=('Times', 14))
        for x in range(29):
            X = 30 * x + 2
            Y = 30 * (x - self.position) + 377
            if x == 12:
                self.create_rectangle(X, 32, X + 30, 65, width=3, outline='red')
                self.create_line(X + 32, 32, X + 60, 32)
                self.create_line(X + 32, 65, X + 60, 65)
            elif x != 13:
                self.create_rectangle(X, 32, X + 30, 65)
            if x < len(self.liste):
                if self.liste[x] == '0':
                    self.create_text(Y, 48, text='0', font=('Times', 18))
                elif self.liste[x] == '1':
                    self.create_text(Y, 48, text='1', font=('Times', 18))


class Cadre(LabelFrame):
    def __init__(self, boss):
        LabelFrame.__init__(self, boss=None)
        self.configure(text="Incrémentation", font=('Times', 12), borderwidth=3)

        self.boss = boss
        self.entier = 0
        self.liste = []

        # Création des variables tkinter
        self.plus_parametres = BooleanVar()
        self.vitesse_defaut = BooleanVar()
        self.mode = IntVar()

        # Création des widgets de base
        self.cadre = Frame(self)
        self.texte = Label(self.cadre, text="Entrer un entier (dec) : ")
        self.entree1 = Entry(self.cadre)
        self.entree2 = Entry(self.cadre)
        self.base = Label(self.cadre, text="Binaire : ")
        self.resultat = Label(self.cadre, text="Résultat : ")
        self.lancer = Button(self.cadre, text="Lancer", command=lambda evt=None: self.lancementAlgo(evt))
        self.parametre = Checkbutton(self.cadre, text="Plus de paramètres", command=self.plusParametres,
                                     variable=self.plus_parametres)

        # Création des widgets supplémentaires
        self.vitesse_par_defaut = Checkbutton(self.cadre, text="Vitesse par défaut", command=self.vitesseDefaut,
                                              variable=self.vitesse_defaut)
        self.vitesse = Scale(self.cadre, orient=HORIZONTAL, length=200, sliderlength=20,
                             tickinterval=350, label="Pause (ms) :", showvalue=0, from_=250, to=1300,
                             troughcolor='light grey', command=self.modifVitesse)
        self.vitesse.set(750)
        self.binaire = Radiobutton(self.cadre, variable=self.mode, value=1, text="Binaire", command=self.modeBinaire)
        self.decimale = Radiobutton(self.cadre, variable=self.mode, value=0, text="Décimale", command=self.modeDecimale)
        self.decimale.select()

        # Placement des widgets
        self.texte.grid(row=1, column=0, padx=10, pady=10, sticky='e')
        self.entree1.grid(row=1, column=1, padx=10, pady=15)
        self.base.grid(row=2, padx=7, pady=3, columnspan=2, sticky='w')
        self.resultat.grid(row=3, padx=7, columnspan=2, sticky='w')
        self.parametre.grid(row=4, pady=10)
        self.lancer.grid(row=4, column=1, padx=5, pady=5, sticky='e')
        self.cadre.grid()

        # Fonction équivalente à un appui sur le bouton 'Lancer'
        self.master.bind('<Return>', self.lancementAlgo)
        self.master.bind('<space>', self.miseEnPause)
        self.master.bind('<x>', self.stopAlgo)
        self.master.bind('<X>', self.stopAlgo)

    def stopAlgo(self, evt):
        self.boss.M.setPause(True)
        self.boss.M.B.setList([])
        self.boss.M.B.setPosition(1)
        self.boss.A = None

    def miseEnPause(self, evt):
        if self.boss.M.getPause():
            self.boss.M.setPause(False)
            print("Reprise")
        else:
            self.boss.M.setPause(True)
            print("Pause")

    def lancementAlgo(self, evt):
        """
        Permet d'afficher le nombre dans la base voulue ainsi que le résultat escompté
        Permet de créer 'self.liste' choisie par l'utilisateur
        Lance l'algorithme choisi
        :param evt: None
        :return: None
        """
        try:
            self.entier = int(self.entree1.get())
            if self.mode.get() == 0:
                self.base.config(text="Binaire : %d" % int(bin(self.entier)[2:]))
                if self.boss.algo == "Incrémentation":
                    self.resultat.config(text="Résultat : %d" % int(bin(self.entier + 1)[2:]))
                self.liste = list(bin(self.entier)[2:])
            if self.mode.get() == 1:
                self.base.config(text="Décimal : %d" % int(self.dec(self.entier)))
                if self.boss.algo == "Incrémentation":
                    self.resultat.config(text="Résultat : %d" % int(bin(int(self.dec(self.entier)) + 1)[2:]))
                self.liste = list(str(self.entier))
            for k in range(len(self.liste)):
                self.liste[k] = self.liste[k]
            self.liste.insert(0, 'B')
            self.liste.append('B')
            self.boss.lancement(self.liste)
        except ValueError:
            print("Entrez un entier valide")

    def dec(self, nb):
        """
        Renvoie l'écriture décimale d'un nombre binaire
        :param nb: entier en écriture binaire
        :return: écriture décimale de 'nb'
        """
        s = 0
        for k in range(len(str(nb))):
            i = int(str(nb)[k])
            if i != 1 and i != 0:
                return "Error"
            s += int(str(nb)[k]) * 2 ** (len(str(nb)) - k - 1)
        return s

    def plusParametres(self):
        """
        Affiche davantage de paramètres, comme la vitesse, le mode (binaire ou décimale)...
        :return: None
        """
        if self.plus_parametres.get():
            self.vitesse.grid(row=5, padx=15, columnspan=2, sticky='w')
            self.binaire.grid(row=6, column=0, padx=20, sticky='w')
            self.decimale.grid(row=6, column=1, sticky='w')
            self.vitesse_par_defaut.grid(row=7)
            self.lancer.grid(row=7)
        else:
            self.vitesse.grid_forget()
            self.binaire.grid_forget()
            self.decimale.grid_forget()
            self.vitesse_par_defaut.grid_forget()
            self.lancer.grid(row=4)

    def vitesseDefaut(self):
        """
        Permet de revenir à la vitesse par défaut si nécessaire
        :return: None
        """
        if self.vitesse_defaut.get():
            self.vitesse.set(750)

    def modeBinaire(self):
        """
        Configuration du mode binaire
        :return: None
        """
        self.texte.configure(text="Entrer un entier (bin) :  ")
        self.base.configure(text="Décimal : ")
        self.resultat.config(text="Résultat :")

    def modeDecimale(self):
        """
        Configuration du mode décimal
        :return: None
        """
        self.texte.configure(text="Entrer un entier (dec) : ")
        self.base.configure(text="Binaire : ")
        self.resultat.config(text="Résultat :")

    def modifVitesse(self, vitesse):
        """
        Permet de récupérer la vitesse choisie par l'utlisitateur
        :param vitesse: int
        :return: None
        """
        if self.vitesse.get() != 750:
            self.vitesse_par_defaut.deselect()
        else:
            self.vitesse_par_defaut.select()
        self.boss.M.setSpeed(self.vitesse.get() / 1000)


class TuringDisplay(Frame):
    def __init__(self, M):
        Frame.__init__(self)
        self.master.title("Machine de Turing")
        self.master.resizable(width=False, height=False)

        self.M = M
        self.A = Incrementation.Incrementation(M)
        self.algo = "Incrémentation"

        # Création des widgets
        self.cadre = Cadre(self)
        self.band = BandDisplay(self)
        self.tableDeTransition = TableDeTransition(self)
        self.choixAlgo = ChoixAlgo(self)

        # Placement des widgets
        self.cadre.grid(row=0, column=0, padx=15, pady=7, sticky='nw')
        self.tableDeTransition.grid(row=0, column=2, rowspan=2, padx=15, pady=7, sticky='ne')
        self.band.grid(columnspan=3, padx=5, pady=5)
        self.choixAlgo.grid(row=0, column=1, pady=17, sticky='n')

        self.band.tracer()
        self.tableDeTransition.tracer()

    def lancement(self, liste):
        if self.A is not None:
            if self.algo == "Addition":
                print("Non disponible")
            else:
                if not self.A.isAlive():
                    self.M.B.setList(liste)
                    self.A.start()
                    power = True
                    while power:
                        print("continue")
                        if not self.A is None:
                            if self.A.isAlive():
                                time.sleep(0.4)
                            else:
                                power = False
                        else:
                            power = False
                        self.band.tracer()
                        self.master.update()
        self.selectAlgo()

    def selectAlgo(self):
        algo = self.M.getAlgorithm()
        print(algo)
        self.A = None
        if algo == "Addition":
            self.cadre.configure(text="Addition")
            self.M.setAlgorithm("Addition")
            print("Non disponible !")

        else:
            if algo == "Incrémentation":
                self.cadre.configure(text="Incrémentation")
                self.M.setAlgorithm("Incrementation")
                self.A = Incrementation.Incrementation(self.M)

            if algo == "Décrémentation":
                self.cadre.configure(text="Décrémentation")
                self.M.setAlgorithm("Decrementation")
                self.A = Decrementation.Decrementation(self.M)

            if algo == "Multiplication par 2":
                self.cadre.configure(text="Multiplication par 2")
                self.M.setAlgorithm("Multiplication")
                self.A = Multiplication.Multiplication(self.M)

            if algo == "Tester la parité":
                self.cadre.configure(text="Tester la parité")
                self.A = Parite.Parite(self.M)

            if algo == "Inverser les 0 et les 1":
                self.cadre.configure(text="Inverser les 0 et 1")
                self.M.setAlgorithm("Inverser les 0 et 1")
                self.A = Inverser.Inverser(self.M)

            if algo == "Doubler une liste de 1":
                self.cadre.configure(text="Doubler une liste de 1")
                self.M.setAlgorithm("Doubler une liste de 1")
                self.A = Doubler.Doubler(self.M)

            if not self.A is None:
                self.M.setTransitionTable(self.A.tableTransition())
                self.tableDeTransition.tracer()
