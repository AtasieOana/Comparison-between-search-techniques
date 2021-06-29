import copy
import math
import os
import sys
import time


class Frunza:
    """
    Clasa reprezentativa pentru frunze
    Atribute:
        idFrunza (string) = identificatorul frunzei
        xFrunza (float) = coordonata x a frunzei
        yFrunza (float)  = coordonata y a frunzei
        nrInsecte (int) = numarul de insecte de pe frunza
        greutateMaxima (float) = greutatea maxima acceptata pe frunza
    """

    def __init__(self, idFrunza, xFrunza, yFrunza, nrInsecte, greutateMaxima):
        """
        Constructorul clasei Frunza
        Argumente:
            idFrunza (string): identificatorul frunzei
            xFrunza (float): coordonata x a frunzei
            yFrunza (float): coordonata y a frunzei
            nrInsecte (int): umarul de insecte de pe frunza
            greutateMaxima (float): greutatea maxima acceptata pe frunza
        """
        self.idFrunza = idFrunza
        self.xFrunza = xFrunza
        self.yFrunza = yFrunza
        self.nrInsecte = nrInsecte
        self.greutateMaxima = greutateMaxima

    def __repr__(self):
        sir = self.idFrunza + "(" + str(self.nrInsecte) + "," + str(self.greutateMaxima) + ")"
        return sir


class Broscuta:
    """
    Clasa reprezentativa pentru broscute
    Atribute:
        numeBroscuta (string)  = numele broscutei
        greutateBroscuta (float) = greutatea broscutei
        idFrunzaBroscuta (string) = identificatorul frunzei pe care se afla broscuta
    """

    def __init__(self, numeBroscuta, greutateBroscuta, idFrunzaStart):
        """
        Constructorul clasei Broscuta
        Argumente:
            numeBroscuta (string): numele broscutei
            greutateBroscuta (float): greutatea broscutei
            idFrunzaStart (string): identificatorul frunzei de pe care pleaca broscuta
        """
        self.numeBroscuta = numeBroscuta
        self.greutateBroscuta = greutateBroscuta
        self.idFrunzaBroscuta = idFrunzaStart

    def __repr__(self):
        sir = self.numeBroscuta + "   " + str(self.greutateBroscuta) + "   " + self.idFrunzaBroscuta
        return sir

    def __eq__(self, other):
        return self.numeBroscuta == other.numeBroscuta and self.greutateBroscuta == other.greutateBroscuta \
               and self.idFrunzaBroscuta == other.idFrunzaBroscuta


class NodParcurgere:
    def __init__(self, info, parinte, cost=0, h=0):
        self.info = info
        self.parinte = parinte
        self.g = cost
        self.h = h
        self.f = round(self.g + self.h, 2)

    def obtineDrum(self):
        l = [self]
        nod = self
        while nod.parinte is not None:
            l.insert(0, nod.parinte)
            nod = nod.parinte
        return l

    def afisDrum(self, iesire, nrMaximNoduri, nrNoduriTotale, afisCost=False, afisLung=False):
        l = self.obtineDrum()
        nodStart = l[0]
        frunzaAnterioara = []
        greutateAnterioara = []
        iesire.write("1)\n")
        for b in nodStart.info[0]:
            if b.idFrunzaBroscuta != "mal":
                indiceFrunza = gaseste_frunza(b, nodStart.info[1])
                frunza = nodStart.info[1][indiceFrunza]
                iesire.write(b.numeBroscuta + " se afla pe frunza initiala " + str(frunza) + ". ")
                frunzaAnterioara.append(frunza)
            else:
                iesire.write(b.numeBroscuta + " se afla pe mal. ")
                frunzaAnterioara.append("mal")
            iesire.write("Greutate broscuta: " + str(b.greutateBroscuta) + "\n")
            greutateAnterioara.append(b.greutateBroscuta)
        iesire.write("Stare frunze: " + str(nodStart.info[1]) + "\n\n")
        nr = 1
        for nod in l[1:]:
            nr += 1
            iesire.write(str(nr) + ")\n")
            (lBroscuta, lFrunza) = nod.info
            for (i, b) in enumerate(lBroscuta):
                if frunzaAnterioara[i] == "mal":
                    continue
                iesire.write(
                    b.numeBroscuta + " a mancat " + str(b.greutateBroscuta - greutateAnterioara[i] + 1) + " insecte. ")
                if b.idFrunzaBroscuta != "mal":
                    indiceFrunza = gaseste_frunza(b, nodStart.info[1])
                    frunza = lFrunza[indiceFrunza]
                    iesire.write(
                        b.numeBroscuta + " a sarit de la " + str(frunzaAnterioara[i]) + " la " + str(frunza) + ". ")
                    frunzaAnterioara[i] = frunza
                else:
                    iesire.write(b.numeBroscuta + " a sarit de la " + str(frunzaAnterioara[i]) + " la mal. ")
                    frunzaAnterioara[i] = "mal"
                iesire.write("Greutate broscuta: " + str(b.greutateBroscuta) + "\n")
                greutateAnterioara[i] = b.greutateBroscuta
            iesire.write("Stare frunze: " + str(lFrunza) + "\n\n")
        if afisCost:
            iesire.write("Cost: " + str(self.g) + "\n")
        if afisLung:
            iesire.write("Lungime: " + str(len(l)) + "\n")
        iesire.write("Numarul maxim de noduri existente la un moment dat in memorie: " + str(nrMaximNoduri) + "\n")
        iesire.write("Numarul total de noduri calculate: " + str(nrNoduriTotale) + '\n')
        return len(l)

    def contineInDrum(self, infoNodNou):
        """
        Functia verifica daca o informatie a mai fost intalnita in drumul nodului curent
        Argumente:
            infoNodNou (([Broscuta][Frunza])): informatia nodului care se doreste a fi adaugat
        Tip returnat:
            True daca lista de broscute din infoNodNou a mai aparut in drumul nodului curent, altfel False
        """
        nod_curent = self
        while nod_curent:
            if nod_curent.info[0] == infoNodNou[0]:
                return True
            nod_curent = nod_curent.parinte
        return False

    def __repr__(self):
        sir = ""
        sir += str(self.info)
        return sir

    def __str__(self):
        sir = ""
        for linie in self.info:
            sir += " ".join([str(elem) for elem in linie]) + "\n"
        sir += "\n"
        return sir

    def __eq__(self, other):
        return self.info == other.info and self.parinte == other.parinte


def gaseste_frunza(broscutaCurenta, listaFrunze):
    """
    Functia gaseste in lista de frunze si returneaza indicele frunzei pe care se afla broscuta curenta
    Argumente:
        broscutaCurenta (obiect de tip Broscuta): broscuta pentru care se cauta frunza pe care se afla
        listaFrunze (lista de obiecte de tip Frunza): lista de frunze in care se cauta frunza
    Tip returnat:
        -1 daca broscuta este pe mal
        i (int): indicele frunzei pe care se afla broscutaCurenta
    """
    if broscutaCurenta.idFrunzaBroscuta == "mal":
        return -1
    for i in range(len(listaFrunze)):
        if listaFrunze[i].idFrunza == broscutaCurenta.idFrunzaBroscuta:
            return i


class Graph:

    def __init__(self, nume_fisier):
        f = open(nume_fisier, "r")
        continutFisier = f.read()
        try:
            self.nrNoduriTotale = 0
            self.nrMaximNoduri = 0
            listaLinii = continutFisier.strip().split("\n")
            self.razaCerc = int(listaLinii[0])
            broscute = listaLinii[1]
            broscuteElemente = broscute.split()
            frunzeGraf = []
            broscuteGraf = []
            if len(broscuteElemente) % 3:
                raise Exception(
                    "Broscutele trebuie sa fie date sub forma: nume, greutate, identificator frunza de start!")
            for numarBroscuta in range(0, len(broscuteElemente), 3):
                broscutaCurenta = (broscuteElemente[numarBroscuta], broscuteElemente[numarBroscuta + 1],
                                   broscuteElemente[numarBroscuta + 2])
                broscuta = Broscuta(broscutaCurenta[0], int(broscutaCurenta[1]), broscutaCurenta[2])
                broscuteGraf.append(broscuta)
            for linie in listaLinii[2:]:
                frunzaElement = linie.split()
                if len(frunzaElement) != 5:
                    raise Exception(
                        "Frunzele trebuie sa fie date sub forma: identificator frunza, coordonata x, coordonata y, "
                        "numar insecte, greutate maxima!")
                frunza = Frunza(frunzaElement[0], int(frunzaElement[1]), int(frunzaElement[2]), int(frunzaElement[3]),
                                int(frunzaElement[4]))
                frunzeGraf.append(frunza)
            self.start = (broscuteGraf, frunzeGraf)

        except Exception as eroare:
            print(eroare)
            sys.exit(0)

    def verifica_mal(self, broscutaCurenta, listaFrunze):
        """
        Functia verifica daca o broscuta poate sari pe mal, tinandu-se cont de faptul ca o broscuta nu poate sari
        mai mult decat greutatea sa impartita la 3
        Argumente:
            broscutaCurenta (obiect de tip Broscuta): broscuta pentru care se verifica daca poate sari la mal
            listaFrunze (lista formata din obiecte de tip Frunza): lista de frunze folosita pentru a gasi frunza
                                                                   pe care se afla broscuta
        Tip returnat:
            1 daca broscuta e pe mal, -1 altfel
        """
        indiceFrunza = gaseste_frunza(broscutaCurenta, listaFrunze)
        frunza = listaFrunze[indiceFrunza]
        if broscutaCurenta.greutateBroscuta / 3 >= self.razaCerc - math.sqrt(frunza.xFrunza ** 2 + frunza.yFrunza ** 2):
            return 1  # broscuta sare la mal
        else:
            return -1  # broscuta nu sare la mal

    def testeaza_scop(self, infoNod):
        for broscuta in infoNod[0]:
            if broscuta.idFrunzaBroscuta != "mal":
                return 0  # nu este stare scop
        return 1  # este stare scop

    def nuAreSolutii(self, infoNod):
        """
        Functie care verifica daca din starea initiala pot fi generate solutii
        Argumente:
            infoNod [(Broscuta, Frunza)]: informatia nodului din care se doreste sa se verifice daca exista solutii
        Tip returnat:
            1 daca problema are solutii, 0 altfel
        """
        for broscuta in infoNod[0]:
            posibil = 0
            indiceFrunza = gaseste_frunza(broscuta, infoNod[1])
            # broscuta e deja pe mal sau poate sari pe mal
            if indiceFrunza == -1 or self.verifica_mal(broscuta, infoNod[1]) == 1:
                continue
            frunzaBroscuta = infoNod[1][indiceFrunza]
            for frunza in infoNod[1]:
                if frunza.idFrunza == frunzaBroscuta.idFrunza:
                    continue
                # daca distanta de la frunza pe care se afla broscuta pana la celelalte frunze este mai mare decat lungimea
                # maxima pe care poate sa o sara broscuta (greutatea/3) + nr de insecte de pe frunza, atunci nu exista solutii
                if math.sqrt(
                        (frunzaBroscuta.xFrunza - frunza.xFrunza) ** 2 + (frunzaBroscuta.yFrunza - frunza.yFrunza) ** 2) \
                        <= broscuta.greutateBroscuta / 3 + frunzaBroscuta.nrInsecte:
                    posibil = 1
                    break
            if posibil == 0:
                return 0  # problema nu are solutii
        return 1  # problema poate avea solutii

    def genereazaSuccesori(self, nodCurent, tip_euristica="euristica banala"):
        """
        Pentru generarea succesurilor, se iau toate broscutele din nodul curent pe rand, fiecare consuma
        un numar de insecte de pe frunza pe care se află, dupa care sare pe alta frunza
        Argumente:
            nodCurent (obiect de tip NodParcurgere): nodul curent din graf
            tip_euristica (str): tipul de euristica care se aplica
        Tip returnat
            listaSuccesori ([([Broscuta][Frunza])]): lista de succesori pentru nodul curent formata din obiecte de tip NodParcurgere
        """
        listaSuccesori = []
        listaBroscute = copy.deepcopy(nodCurent.info[0])
        listaFrunze = copy.deepcopy(nodCurent.info[1])
        listePerechi = []
        listaBroscuteFrunze = [(listaBroscute, listaFrunze)]
        for (b, broscutaCurenta) in enumerate(listaBroscute):
            indiceFrunzaCurent = gaseste_frunza(broscutaCurenta, nodCurent.info[1])
            # broscuta e deja la mal
            if indiceFrunzaCurent == -1:
                continue
            perechiAccesibileFrunzaCurenta = []
            for nrInsecteMancate in range(0, nodCurent.info[1][indiceFrunzaCurent].nrInsecte + 1):
                copieBroscutaCurenta = copy.deepcopy(broscutaCurenta)
                copieFrunzaCurenta = copy.deepcopy(nodCurent.info[1][indiceFrunzaCurent])
                # broscuta mananca un numar de insecte de pe frunza pe care se afla
                greutate_noua = copieBroscutaCurenta.greutateBroscuta + nrInsecteMancate

                copieBroscutaCurenta.greutateBroscuta = greutate_noua
                copieFrunzaCurenta.nrInsecte -= nrInsecteMancate

                # cautam frunzele accesibile pentru broscuta
                for perecheBroscuteFrunze in listaBroscuteFrunze:
                    perecheBroscuteFrunze[0][b] = copy.deepcopy(copieBroscutaCurenta)
                    perecheBroscuteFrunze[1][indiceFrunzaCurent] = copy.deepcopy(copieFrunzaCurenta)
                    perechiBroscuteFrunzeAccesibile = self.gaseste_frunze_accesibile_pentru_broscuta(
                        copieBroscutaCurenta, perecheBroscuteFrunze, b)
                    if not perechiBroscuteFrunzeAccesibile:
                        continue
                    for p in perechiBroscuteFrunzeAccesibile:
                        perechiAccesibileFrunzaCurenta.append(p)

            listaBroscuteFrunze = copy.deepcopy(perechiAccesibileFrunzaCurenta)

        for pereche in listaBroscuteFrunze:
            if not nodCurent.contineInDrum(pereche) and pereche[0] not in listePerechi:
                # calculam costul pentru noul nod
                distantaAdunata = 0
                for (b, broscuta) in enumerate(pereche[0]):
                    indiceFrunzaActuala = gaseste_frunza(broscuta, pereche[1])
                    indiceFruzaVeche = gaseste_frunza(nodCurent.info[0][b], nodCurent.info[1])
                    # broscuta era deja la mal
                    if indiceFruzaVeche == -1:
                        continue
                    frunzaVeche = nodCurent.info[1][indiceFruzaVeche]
                    if indiceFrunzaActuala == -1:  # broscuta a sarit la mal
                        distantaAdunata += (
                                self.razaCerc - math.sqrt(frunzaVeche.xFrunza ** 2 + frunzaVeche.yFrunza ** 2))
                    else:
                        frunzaActuala = pereche[1][indiceFrunzaActuala]
                        distantaAdunata += math.sqrt((frunzaVeche.xFrunza - frunzaActuala.xFrunza) ** 2 + (
                                frunzaVeche.yFrunza - frunzaActuala.yFrunza) ** 2)
                costMutare = round((nodCurent.g + distantaAdunata), 2)
                listaSuccesori.append(
                    NodParcurgere(pereche, nodCurent, costMutare, self.calculeaza_h(pereche, tip_euristica)))
                listePerechi.append(pereche[0])
        self.nrNoduriTotale += len(listaSuccesori)
        return listaSuccesori

    def gaseste_frunze_accesibile_pentru_broscuta(self, broscutaCurenta, perecheCurentaBroscuteFrunze,
                                                  indiceBroscutaCurenta):
        """
        Pentru o broscuta primita ca parametru se cauta toate frunzele pe care aceasta poate sa sara de pe frunza curenta
        Argumente:
            broscutaCurenta (obiect de tip Broscuta): broscuta pentru care se cauta frunzele accesibile
            perecheCurentaBroscuteFrunze (([Broscuta][Frunza])): lista de broscute necesara pentru calcularea greutatii
                                                                de pe o frunza si lista de frunze pentru parcurgere
            indiceBroscutaCurenta (int): indicele broscutei curente din lista de broscute
        Tip returnat
            perechiBroscuteFrunzeAccesibile ([([Broscuta][Frunza])]): lista care retine informatia pentru posibili succesori
        """
        if broscutaCurenta.idFrunzaBroscuta == "mal":
            return [perecheCurentaBroscuteFrunze]
        perechiBroscuteFrunzeAccesibile = []
        listaFrunze = copy.deepcopy(perecheCurentaBroscuteFrunze[1])
        indiceFrunzaCurent = gaseste_frunza(broscutaCurenta, listaFrunze)
        frunzaCurenta = listaFrunze[indiceFrunzaCurent]
        # broscuta poate sari pe mal
        if self.verifica_mal(broscutaCurenta, listaFrunze) == 1:
            listaBroscute = copy.deepcopy(perecheCurentaBroscuteFrunze[0])
            copieBroscutaCurenta = copy.deepcopy(broscutaCurenta)
            copieBroscutaCurenta.idFrunzaBroscuta = "mal"
            copieBroscutaCurenta.greutateBroscuta -= 1
            listaBroscute[indiceBroscutaCurenta] = copieBroscutaCurenta
            perechiBroscuteFrunzeAccesibile.append((listaBroscute, listaFrunze))
            return perechiBroscuteFrunzeAccesibile
        for (i, frunza) in enumerate(listaFrunze):
            listaBroscute = copy.deepcopy(perecheCurentaBroscuteFrunze[0])
            copieBroscutaCurenta = copy.deepcopy(broscutaCurenta)
            if frunza.idFrunza == frunzaCurenta.idFrunza:
                continue
            # broscuta a ajuns la greutatea 0
            if copieBroscutaCurenta.greutateBroscuta - 1 < 1:
                continue
            # calculam greutatea ce se afla pe frunza
            greutateFrunza = 0
            for broscuta in perecheCurentaBroscuteFrunze[0]:
                if broscuta.idFrunzaBroscuta == frunza.idFrunza:
                    greutateFrunza += broscuta.greutateBroscuta
            greutateFrunza += frunza.nrInsecte
            # daca broscuta ar sari pe frunza si s-ar depasi greutatea maxima admisa de pe frunza
            if frunza.greutateMaxima - greutateFrunza < copieBroscutaCurenta.greutateBroscuta - 1:
                continue

            # lungimea unei sarituri de broscuta e maxim valoarea greutatii/3
            if math.sqrt((frunzaCurenta.xFrunza - frunza.xFrunza) ** 2 + (frunzaCurenta.yFrunza - frunza.yFrunza) ** 2) \
                    > copieBroscutaCurenta.greutateBroscuta / 3:
                continue

            # broscuta poate sari pe frunza
            copieBroscutaCurenta.idFrunzaBroscuta = frunza.idFrunza
            copieBroscutaCurenta.greutateBroscuta -= 1
            listaBroscute[indiceBroscutaCurenta] = copieBroscutaCurenta
            perechiBroscuteFrunzeAccesibile.append((listaBroscute, listaFrunze))
        return perechiBroscuteFrunzeAccesibile

    def calculeaza_h(self, infoNod, tip_euristica="euristica banala"):
        if self.testeaza_scop(infoNod):
            return 0
        if tip_euristica == "euristica banala":
            return 1
        if tip_euristica == "euristica admisibila 1":
            # h = minimul dintre distantele de la frunzele pe care se afla broscutele pana la cel mai apropiat mal
            minim = float('inf')
            for broscuta in infoNod[0]:
                indiceFrunza = gaseste_frunza(broscuta, infoNod[1])
                if indiceFrunza == -1:
                    continue
                frunza = infoNod[1][indiceFrunza]
                distantaMal = self.razaCerc - math.sqrt(frunza.xFrunza ** 2 + frunza.yFrunza ** 2)
                if distantaMal < minim:
                    minim = distantaMal
            return minim
        elif tip_euristica == "euristica admisibila 2":
            # h = maximul dintre distantele de la frunzele pe care se afla broscutele pana la cel mai apropiat mal
            maxim = 0
            for broscuta in infoNod[0]:
                indiceFrunza = gaseste_frunza(broscuta, infoNod[1])
                if indiceFrunza == -1:
                    continue
                frunza = infoNod[1][indiceFrunza]
                distantaMal = self.razaCerc - math.sqrt(frunza.xFrunza ** 2 + frunza.yFrunza ** 2)
                if distantaMal > maxim:
                    maxim = distantaMal
            return maxim
        else:
            # h = suma tuturor distantelor de la frunzele pe care se afla broscutele pana la cel mai îndepartat mal
            suma = 0
            for broscuta in infoNod[0]:
                indiceFrunza = gaseste_frunza(broscuta, infoNod[1])
                if indiceFrunza == -1:
                    continue
                frunza = infoNod[1][indiceFrunza]
                distantaMal = self.razaCerc + math.sqrt(frunza.xFrunza ** 2 + frunza.yFrunza ** 2)
                suma += distantaMal
            return suma

    def __repr__(self):
        sir = ""
        for (k, v) in self.__dict__.items():
            sir += "{} = {}\n".format(k, v)
        return sir


def uniform_cost(gr, iesire, nrSolutiiCautate, timeout):
    t1 = time.time()
    nr = 1
    if gr.nuAreSolutii(gr.start) == 0:
        iesire.write("Nu are solutii!\n")
        return
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    gr.nrNoduriTotale += 1
    while len(c) > 0:
        gr.nrMaximNoduri = max(gr.nrMaximNoduri, len(c))
        current_time = time.time()
        if round(current_time - t1) > timeout:
            iesire.write("Timeout!\n")
            return
        nodCurent = c.pop(0)
        if gr.testeaza_scop(nodCurent.info):
            iesire.write("Solutie: " + str(nr) + "\n")
            nodCurent.afisDrum(iesire, gr.nrMaximNoduri, gr.nrNoduriTotale, afisCost=True, afisLung=True)
            nrSolutiiCautate -= 1
            t2 = time.time()
            milis = round(1000 * (t2 - t1))
            iesire.write("\nTimpul de gasire a solutiei: {} milisecunde. \n---------\n".format(milis))
            nr += 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].g > s.g:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def a_star(gr, iesire, nrSolutiiCautate, timeout, tip_euristica):
    t1 = time.time()
    nr = 1
    if gr.nuAreSolutii(gr.start) == 0:
        iesire.write("Nu are solutii!\n")
        return
    c = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    gr.nrNoduriTotale += 1
    while len(c) > 0:
        gr.nrMaximNoduri = max(gr.nrMaximNoduri, len(c))
        current_time = time.time()
        if round(current_time - t1) > timeout:
            iesire.write("Timeout!\n")
            return
        nodCurent = c.pop(0)
        if gr.testeaza_scop(nodCurent.info):
            iesire.write("Solutie: " + str(nr) + "\n")
            nodCurent.afisDrum(iesire, gr.nrMaximNoduri, gr.nrNoduriTotale, afisCost=True, afisLung=True)
            nrSolutiiCautate -= 1
            t2 = time.time()
            milis = round(1000 * (t2 - t1))
            iesire.write("\nTimpul de gasire a solutiei: {} milisecunde. \n---------\n".format(milis))
            nr += 1
            if nrSolutiiCautate == 0:
                return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                if c[i].f >= s.f or (c[i].f == s.f and c[i].g <= s.g):
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)


def a_star_optimizat(gr, iesire, timeout, tip_euristica):
    t1 = time.time()
    if gr.nuAreSolutii(gr.start) == 0:
        iesire.write("Nu are solutii!\n")
        return
    lista_open = [NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))]
    lista_closed = []
    gr.nrNoduriTotale += 1
    while len(lista_open) > 0:
        current_time = time.time()
        if round(current_time - t1) > timeout:
            iesire.write("Timeout!\n")
            return
        nodCurent = lista_open.pop(0)
        lista_closed.append(nodCurent)
        if gr.testeaza_scop(nodCurent.info):
            iesire.write("Solutie: \n")
            nodCurent.afisDrum(iesire, gr.nrMaximNoduri, gr.nrNoduriTotale, afisCost=True, afisLung=True)
            t2 = time.time()
            milis = round(1000 * (t2 - t1))
            iesire.write("\nTimpul de gasire a solutiei: {} milisecunde. \n---------\n".format(milis))
            return
        lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica)
        for s in lSuccesori:
            gasitC = False
            for nodC in lista_open:
                if s.info == nodC.info:
                    gasitC = True
                    if s.f >= nodC.f:
                        lSuccesori.remove(s)
                    else:  # s.f<nodC.f
                        lista_open.remove(nodC)
                    break
            if not gasitC:
                for nodC in lista_closed:
                    if s.info == nodC.info:
                        if s.f >= nodC.f:
                            lSuccesori.remove(s)
                        else:  # s.f<nodC.f
                            lista_closed.remove(nodC)
                        break
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(lista_open)):
                if lista_open[i].f > s.f or (lista_open[i].f == s.f and lista_open[i].g <= s.g):
                    gasit_loc = True
                    break
            if gasit_loc:
                lista_open.insert(i, s)
            else:
                lista_open.append(s)
        gr.nrMaximNoduri = max(gr.nrMaximNoduri, (len(lista_open) + len(lista_closed)))


global nr, nrMaximNoduriIDAStar


def ida_star(gr, iesire, nrSolutiiCautate, timeout, tip_euristica):
    t1 = time.time()
    if tip_euristica == "euristica neadmisibila":
        nrSolutiiCautate = 1
    global nr
    nr = 1
    if gr.nuAreSolutii(gr.start) == 0:
        iesire.write("Nu are solutii!\n")
        return
    nodStart = NodParcurgere(gr.start, None, 0, gr.calculeaza_h(gr.start))
    limita = nodStart.f
    while True:
        gr.nrNoduriTotale += 1
        nrSolutiiCautate, rez = construieste_drum(gr, nodStart, limita, nrSolutiiCautate, t1, tip_euristica, timeout)
        if rez == "stop":
            break
        if rez == float('inf'):
            iesire.write("Nu exista suficiente solutii! \n")
            break
        limita = rez


def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate, t1, tip_euristica, timeout):
    global nrMaximNoduriIDAStar
    current_time = time.time()
    if round(current_time - t1) > timeout:
        iesire.write("Timeout!\n")
        return 0, "stop"
    global nr
    if nodCurent.f > limita:
        return nrSolutiiCautate, nodCurent.f
    if gr.testeaza_scop(nodCurent.info) and (nodCurent.f == limita or tip_euristica == "euristica neadmisibila"):
        iesire.write("Solutie: " + str(nr) + "\n")
        nodCurent.afisDrum(iesire, gr.nrMaximNoduri, gr.nrNoduriTotale, afisCost=True, afisLung=True)
        nrSolutiiCautate -= 1
        t2 = time.time()
        milis = round(1000 * (t2 - t1))
        iesire.write("\nTimpul de gasire a solutiei: {} milisecunde. \n---------\n".format(milis))
        nr += 1
        if nrSolutiiCautate == 0:
            return 0, "stop"
    lSuccesori = gr.genereazaSuccesori(nodCurent, tip_euristica=tip_euristica)
    gr.nrMaximNoduri = max(gr.nrMaximNoduri, len(lSuccesori))
    minim = float('inf')
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum(gr, s, limita, nrSolutiiCautate, t1, tip_euristica, timeout)
        if rez == "stop":
            return 0, "stop"
        if rez < minim:
            minim = rez
    return nrSolutiiCautate, minim


# citirea din linia de comanda
cale_fisier_intrare = sys.argv[1]
cale_fisier_iesire = sys.argv[2]
nrSolutii = int(sys.argv[3])
timeout = int(sys.argv[4])


def construiesteGraf(inputFile):
    """
    Functie care construieste un graf folosind datele dintr-un fisier de input
    Argumente:
        inputFile (str): numele fisierului de intrare
    Tip returnat
        gr (obiect de tip Graph): graf initializat folosind datele din fisierul de input
    """
    try:
        os.chdir(cale_fisier_intrare)
    except FileNotFoundError:
        sys.exit("Folder-ul {0} nu exista".format(cale_fisier_intrare))
    except NotADirectoryError:
        sys.exit("{0} nu duce la un folder".format(cale_fisier_intrare))
    gr = Graph(inputFile)
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)
    try:
        os.chdir(cale_fisier_iesire)
    except FileNotFoundError:
        sys.exit("Folder-ul {0} nu exista".format(cale_fisier_iesire))
    except NotADirectoryError:
        sys.exit("{0} nu duce la un folder".format(cale_fisier_iesire))
    return gr


def schimbaFisierele(inputFile):
    """
    Functie care realizeaza schimbarile de direct dintre Input si Output si construieste un graf folosind datele
    dintr-un fisier de input
    Argumente:
        inputFile (str): numele fisierului de intrare
    Tip returnat
        gr (obiect de tip Graph): graf initializat folosind datele din fisierul de input
    """
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)
    gr = construiesteGraf(inputFile)
    if not os.path.isdir("OutputFor" + inputFile):
        os.mkdir("OutputFor" + inputFile)
    os.chdir("OutputFor" + inputFile)
    return gr


for inputFile in ["Input_a_fara_solutii.txt", "Input_b_stare_initiala_finala.txt", "Input_c_fara_blocaj.txt",
                  "Input_d_cu_blocaj.txt"]:
    gr = construiesteGraf(inputFile)
    if not os.path.isdir("OutputFor" + inputFile):
        os.mkdir("OutputFor" + inputFile)
    os.chdir("OutputFor" + inputFile)
    # afisarea output-ului pentru UCS
    fisier_iesire_UCS = "OutputUCS.txt"
    iesire = open(fisier_iesire_UCS, "w")
    iesire.write("Solutii obtinute cu UCS: \n")
    uniform_cost(gr, iesire, nrSolutii, timeout)
    # afisarea output-ului pentru A*
    gr = schimbaFisierele(inputFile)
    fisier_iesire_AStar = "OutputAStar.txt"
    iesire = open(fisier_iesire_AStar, "w")
    iesire.write("Solutii obtinute cu A*: \n")
    iesire.write("\n\nEuristica banala: \n")
    a_star(gr, iesire, nrSolutii, timeout, tip_euristica="euristica banala")
    gr = schimbaFisierele(inputFile)
    iesire.write("\n\nEuristica admisibila 1: \n")
    a_star(gr, iesire, nrSolutii, timeout, tip_euristica="euristica admisibila 1")
    gr = schimbaFisierele(inputFile)
    iesire.write("\n\nEuristica admisibila 2: \n")
    a_star(gr, iesire, nrSolutii, timeout, tip_euristica="euristica admisibila 2")
    gr = schimbaFisierele(inputFile)
    iesire.write("\n\nEuristica neadmisibila: \n")
    a_star(gr, iesire, nrSolutii, timeout, tip_euristica="euristica neadmisibila")
    # afisarea output-ului pentru A* optimizat
    gr = schimbaFisierele(inputFile)
    fisier_iesire_AStar_Optimizat = "OutputAStarOptimizat.txt"
    iesire = open(fisier_iesire_AStar_Optimizat, "w")
    iesire.write("Solutii obtinute cu A* optimizat: \n")
    iesire.write("\n\nEuristica banala: \n")
    a_star_optimizat(gr, iesire, timeout, tip_euristica="euristica banala")
    gr = schimbaFisierele(inputFile)
    iesire.write("\n\nEuristica admisibila 1: \n")
    a_star_optimizat(gr, iesire, timeout, tip_euristica="euristica admisibila 1")
    gr = schimbaFisierele(inputFile)
    iesire.write("\n\nEuristica admisibila 2: \n")
    a_star_optimizat(gr, iesire, timeout, tip_euristica="euristica admisibila 2")
    gr = schimbaFisierele(inputFile)
    iesire.write("\n\nEuristica neadmisibila: \n")
    a_star_optimizat(gr, iesire, timeout, tip_euristica="euristica neadmisibila")
    # afisarea output-ului pentru IDA*
    gr = schimbaFisierele(inputFile)
    fisier_iesire_IDAStar = "OutputIDAStar.txt"
    iesire = open(fisier_iesire_IDAStar, "w")
    iesire.write("Solutii obtinute cu IDA*: \n")
    iesire.write("\n\nEuristica banala: \n")
    ida_star(gr, iesire, nrSolutii, timeout, tip_euristica="euristica banala")
    gr = schimbaFisierele(inputFile)
    iesire.write("\n\nEuristica admisibila 1: \n")
    ida_star(gr, iesire, nrSolutii, timeout, tip_euristica="euristica admisibila 1")
    gr = schimbaFisierele(inputFile)
    iesire.write("\n\nEuristica admisibila 2: \n")
    ida_star(gr, iesire, nrSolutii, timeout, tip_euristica="euristica admisibila 2")
    gr = schimbaFisierele(inputFile)
    iesire.write("\n\nEuristica neadmisibila: \n")
    ida_star(gr, iesire, nrSolutii, timeout, tip_euristica="euristica neadmisibila")
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)
    path_parent = os.path.dirname(os.getcwd())
    os.chdir(path_parent)
