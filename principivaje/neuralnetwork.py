# -*- coding: utf-8 -*-
import numpy as np
import math
from collections import namedtuple


#print w_1
#print w_2
#print vhod_1
class Nevronska_mreza(object):

    def __init__(self, eta, vhod_1, zeleni_izhod, w_1, w_2, i, j, l):
        Neuron = namedtuple("Neuron", "utez")
        vhod_1 = np.array(vhod_1)
        bias = np.zeros((vhod_1.shape[0], 1)) - 1
        vhod_1 = np.hstack((bias, vhod_1))
        self.eta = eta
        self.vhod_1 = np.array(vhod_1)
        self.zeleni_izhod = np.array(zeleni_izhod)
        self.w_1 = np.array(w_1)
        self.w_2 = np.array(w_2)
        if self.vhod_1.shape[1] != self.w_1.shape[1]:
            raise Exception(u"Dolžina vhoda in število uteži v prvem nivoju mora biti enako!")
        if self.vhod_1.shape[0] != self.zeleni_izhod.shape[0]:
            raise Exception(
                u"Število vhodov mora biti enako številu želenih izhodov")
        self.i = i
        self.j = j
        self.l = l
        self.text_izhod = []
        self.tabela = []
        neuroni_1 = [Neuron(utez=(i, 1)) for i in range(1, self.w_1.shape[0] + 1)]

        neuroni_2 = [Neuron(utez=(i, 1)) for i in range(1, self.w_2.shape[0] + 1)]

        self.neuroni = [neuroni_1, neuroni_2]
        header = ["p"]
        self.length_input = self.vhod_1.shape[1]
        self.length_last_layer = self.w_2.shape[0]
        for i in range(1, self.length_input):
            header.append("\(x_%d^{(p)}\)" % i)
        for i in range(1, self.length_last_layer + 1):
            header.append("\(o_%d^{(p)}\)" % i)
        for i in range(1, self.length_last_layer + 1):
            header.append("\(d_%d^{(p)}\)" % i)
        for i in range(1, 3):
            header.append("\(\delta_%d^{(2)}\)" % i)
        for i in range(1, 4):
            header.append("\(\delta_%d^{(1)}\)" % i)
        header.append("\(w_{%d,%d}^{(%d)}\)" % (self.i, self.j, self.l))
        self.tabela.append(header)
        for i in range(self.vhod_1.shape[0]):
            rezultati = [i + 1]
            rezultati.extend(self.vhod_1[i, 1:])
            rezultati.extend([" "] * self.length_last_layer)
            rezultati.extend(self.zeleni_izhod[i, :])
            rezultati.extend([" "] * 6)
            self.tabela.append(rezultati)
        self.deltas = {}

    @staticmethod
    def perceptron(w, vhod):
        def to_str(x):
            if x < 0:
                return "(%0.6f)" % x
            else:
                return "%0.6f" % x
        izhod = []
        izpis = "%s \cdot %s"
        str_vhod = map(to_str, vhod)
        str_w = map(to_str, w)
        izhod = map(lambda x: izpis % x, zip(str_w, str_vhod))
        str_izhod = " + ".join(izhod)

        v = (w.T * vhod).sum()
        str_izhod += " = %.6f" % v
        return v, str_izhod

    @staticmethod
    def logisticni_neuron(z):
        return 1.0 / (1.0 + math.exp(-z))

    def run(self):
        self.vhod_2 = None
        self.delta_i_2 = np.zeros(
            (self.vhod_1.shape[0], self.zeleni_izhod.shape[1]))
        self.izhod = None
        w_pop = 0
# Za vsak učni vzorec
# ko se izvede cela zanka se izvede ena epoha
        for index_primer in range(self.vhod_1.shape[0]):
            self.text_izhod.append(
                u"<h3>Učni vzorec %d</h3>" % (index_primer + 1))
#Izracunajo se izhodi iz skritega nivoja
            self.vhod_2 = self.nivo(
                index_primer, 0, self.vhod_1, self.w_1, self.vhod_2)
            #print self.vhod_2
#izracunajo se izhodi iz zunanjega nivoja
            self.izhod = self.nivo(
                index_primer, 1, self.vhod_2, self.w_2, self.izhod)
            #print "izhod"
            #print self.izhod
#Tabela se napolni z izhodom iz nevronske mreze
            st_vhodov = self.vhod_1.shape[1] - 1
            for i in range(self.izhod.shape[0]):
                for j in range(1, self.izhod.shape[1]):
                    self.tabela[i + 1][st_vhodov + j] = self.izhod[i, j]
#Začne se backpropagation
            self.text_izhod.append(u"<h3>Računanje popravka uteži</h3>")
            self.index_primer = index_primer
# FIXME: to ma nepotrebne vhodne parametre
            w_tren = self.popravki_utezi(self.i, self.j, self.l,
                                         self.vhod_1[index_primer], self.vhod_2[index_primer],
                                         self.izhod[index_primer],
                                         self.zeleni_izhod[index_primer])
            self.tabela[index_primer + 1][-1] = "%0.6f" % (w_tren,)
# Skupen popravek uteži
            w_pop += w_tren
# Napolni se tabela z ostalimi deltami
# vse niso potrebne za računanje popravka želene uteži
            self.text_izhod.append(
                u"<h3>Računanje vseh želenih \(\delta\) vrednosti</h3>")
            self.text_izhod.append(u"<p>Te vrednosti niso potrebne za računanje popravkov uteži. Izračunane so zato, ker so bile v primeru</p>")
            for index_tabela, (j, l) in enumerate([(1, 2), (2, 2), (1, 1), (2, 1), (3, 1)]):
                var = self.deltas.get("%d_%d" % (j, l), None)
                if var is None:
                    try:
                        var = self.delta(j, l, self.vhod_1[index_primer],
                                        self.vhod_2[index_primer],
                                        self.izhod[index_primer],
                                        self.zeleni_izhod[index_primer])
                    except Exception, ex:
                        var = 0
                self.tabela[1 + index_primer][
                    index_tabela + self.length_input + self.length_last_layer*2] = "%0.6f" % (var,)
            self.deltas = {}
        self.text_izhod.append("Skupni popravek utezi \(w_{{{i},{j}}}^{{({l})}} = {w:0.6f}\)".format(w=w_pop, i=self.i, j=self.j, l=self.l))

    def nivo(self, indeks_primera, indeks_nivo, vhod, utezi, vhod_2=None):
        """izracuna za en vhodni primer izhode vseh nevronov v plasti"""
        if vhod_2 is None:
            vhod_2 = np.zeros(
                (vhod.shape[0], len(self.neuroni[indeks_nivo]) + 1))
            #dodamo bias na izhod
            #Ta izhod namreč postane vhod v naslednji plasti
            vhod_2[:, 0] = - 1
        self.text_izhod.append("<h4>%d nivo</h4>" % (indeks_nivo + 1))
# Za vsak nevron
        for index, neuron in enumerate(self.neuroni[indeks_nivo]):
            utez = neuron.utez
            self.text_izhod.append("<h5>Nevron %d</h5>" % (index + 1,))
            v, str_izhod = self.perceptron(
                utezi[utez[0] - 1], vhod[indeks_primera])
            self.text_izhod.append(
                "$$v_%d^{(%d)} = %s$$" % (utez[0], utez[1], str_izhod))
            y = Nevronska_mreza.logisticni_neuron(v)
            #import pdb; pdb.set_trace()
            self.text_izhod.append(
                "$$y_%d^{(%d)} = %0.6f$$" % (utez[0], utez[1], y))
            vhod_2[indeks_primera, utez[0]] = round(y, 6)
        return vhod_2

    def delta(self, j, l, vhod, izhod_s_nivo, izhod_nivo, zeleni_izhod_i):
        """Izračunava želeno delto in vse y-one in delte,ki so potrebni za ta izračun
        za popravljanje napak"""
        start = "$$\delta_{j}^{{({l})}} = y_{j}^{{{l}}} \\times (1-y_{j}^{{{l}}})"
        start_vals = "$$\delta_{j}^{{({l})}} = {y: 0.6f} \\times (1 - {y: 0.6f})"
        # računa za zadnji nivo
        if l == 2:
            o_i = izhod_nivo[j]
            d_i = zeleni_izhod_i[j - 1]
            rez = o_i * (1 - o_i) * (d_i - o_i)
            tmp = start.replace("y", "o") + " \\times (d_{j} - o_{j})$$"
            vals = start_vals + "\\times ({d} - {y: 0.6f}) = {rez: 0.6f}$$"
            self.text_izhod.append(tmp.format(j=j, l=l))
            self.text_izhod.append(
                vals.format(j=j, l=l, y=o_i, d=d_i, rez=rez))
            self.deltas["%d_%d" % (j, l)] = rez
        # računa za ostale nivoje
        else:
            y_j_l = self.y(j, l, vhod)
            # FIXME: trenutno dela samo za logistične nevrone
            rez = y_j_l * (1 - y_j_l)
            tmp = start + " \\times ("
            vals = start_vals + " \\times ("
            k = 1
            wk = []
            wk_vals = []
            rez_vals = []
            # računanje: (\Epsilon_k w_k,j^(l+1) \delta_k^(l+1))
            for utez in self.w_2[:, j]:
                if utez != 0:
                    wk.append("w_{{" + str(k) + ",{j}}}^{{({l_1})}} \\times \delta_" + str(k) + "^{{({l_1})}}")
                    delta_j_l_1 = self.delta(
                        k, l + 1, vhod, izhod_s_nivo, izhod_nivo, zeleni_izhod_i)
                    wk_vals.append("%.6f \\times %.6f" % (utez, delta_j_l_1))
                    rez_vals.append(utez * delta_j_l_1)
                    k += 1
            tmp += "+".join(wk)
            vals += "+".join(wk_vals)
            rez *= sum(rez_vals)

            tmp += ")$$"
            vals = vals + ") = {rez: 0.6f}$$"
            self.text_izhod.append(tmp.format(j=j, l=l, l_1=l + 1))
            self.text_izhod.append(vals.format(j=j, l=l, y=y_j_l, rez=rez))
            self.deltas["%d_%d" % (j, l)] = rez
        return rez

    def y(self, j, l, vhod):
        """pridobi vrednosti y_j^(l), ki so potrebni za računanje popravkov uteži"""
        rez = 42
# y_0^(l) = - 1
        if j == 0:
            self.text_izhod.append("$$y_0^{%d} = -1$$" % (l))
            rez = -1
            return rez
# y_j^(0) = x_j
        if l == 0:
            rez = vhod[j]
            self.text_izhod.append(
                "$$y_{j}^{{0}} = x_{j} = {rez: 0.6f}$$".format(j=j, rez=rez))
            return rez
        start = "$$y_{j}^{{{l}}} = "
# y_j^(l) je rezultat nekje v skriti plasti
        if l == 1:
            rez = self.vhod_2[self.index_primer, j]
            tmp = start + "{rez: 0.6f}$$"
            self.text_izhod.append(tmp.format(j=j, l=l, rez=rez))
        return rez

    def popravki_utezi(self, i, j, l, vhod, izhod_s_nivo, izhod_nivo, zeleni_izhod_i):
        """Izračuna popravke uteži za utež w_i,j^(l) indeksi so enaki
        kot na predavanjih"""
        delta_j_l = self.delta(
            i, l, vhod, izhod_s_nivo, izhod_nivo, zeleni_izhod_i)
        y_j_l = self.y(j, l - 1, vhod)
        rez = self.eta * delta_j_l * y_j_l
        self.text_izhod.append("$$\Delta w_{{{i},{j}}}^{{({l})}} = \eta \cdot \delta_{i}^{{({l})}}y_{j}^{l_1}$$".format(i=i, j=j, l=l, l_1=l - 1))
        self.text_izhod.append("$$\Delta w_{{{i},{j}}}^{{({l})}} = {eta: .6f} \cdot {delta: 0.6f} \cdot {y: 0.6f} = {rez: 0.6f}$$".format(i=i, j=j, l=l, eta=self.eta, delta=delta_j_l, rez=rez, y=y_j_l))
        return rez


if __name__ == "__main__":
# Vsi podatki so podatki iz predavanj na strani 23
    eta = 0.3
#stolpci vhodni nevroni brez biasa
#vsaka vrstica je en primer
    vhod_1 = [
        [0, 0.4, -0.2],
        [0.3, -0.1, 0.5]
    ]

    zeleni_izhod = np.array([
        [0, 1],
        [1, 0]
    ])

    """Uteži so vse uteži od 0 do n, če nekatere v navodilih manjkajo moraju

    Tukaj imeti vrednost 0"""

#Uteži prvega nivoja
    w_1 = np.array([
        [0, 0.2, -0.2, 0],
        [0, 0.1, 0, 0.5],
        [0, -0.3, 0, 0.4]
    ])

#Uteži drugega nivoja
    w_2 = np.array([
        [0, 0.5, -0.5, 0],
        [0, 0, -0.3, 0.8],
    ])
    nn = Nevronska_mreza(0.3, vhod_1, zeleni_izhod, w_1, w_2, 1, 2, 1)
    nn.run()
    print nn.tabela[0]
    #for text in nn.text_izhod:
        #print text

    eta = 0.5

    vhod_1 = [
        [0.5, -0.4]
    ]

    zeleni_izhod = [
        [0]
    ]

    w_1 = [
        [0.3, -0.4, 0],
        [0, 0.6, 0.5]
    ]

    w_2 = [
        [0.5, -0.5, 0.7]
    ]

    nn = Nevronska_mreza(eta, vhod_1, zeleni_izhod, w_1, w_2, 1,1,2)
    print nn.tabela[0]
    nn.run()
    for text in nn.text_izhod:
        print text
