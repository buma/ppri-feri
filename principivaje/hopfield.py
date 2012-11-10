# -*- coding: utf-8 -*-
import numpy as np
from itertools import product as iproduct


class Hopfield(object):

    def __init__(self, w, function_type=0, text_output=[]):
        """Delta learning algorithm

        w - numpy array of weights
        """
        self.text_output = text_output
        self.text_output.append(u"<h2>Sinhrono učenje</h2>")
        self.weight = np.array(w)
        self.function_type = function_type
        if function_type == 0:
            self.y_func = self.y_i_0
            self.text_output.append(r"$$y =  \left\{\begin{matrix} 0 & \mbox {if } v < 0, \\ 1 & \mbox{if } v > 0, \\ \text{enako kot prej} & \mbox{if } v=0\end{matrix}\right.$$")
        elif function_type == 1:
            self.y_func = self.y_i_1
            self.text_output.append(r"$$y =  \left\{\begin{matrix} -1 & \mbox {if } v < 0, \\ +1 & \mbox{if } v > 0, \\ \text{enako kot prej} & \mbox{if } v=0\end{matrix}\right.$$")
            self.text_output.append(u'<span class="label label-warning">Opozorilo</span>Ta funkcija je še v beta stanju. Nevem namreč kako računat oznake</p>')
        else:
            raise Exception("Invalid function: %d!" % (function_type,))
        self.table = []
        self.number_of_weights = len(w)
        weights_label = ["\(y_%d\)" % i for i in range(1,
                                                       self.number_of_weights + 1)]
        header = weights_label + ["Oznaka"] + weights_label + ["Oznaka"]
        self.table.append(header)

    def y_i_1(self, v_i, y_before):
        retval = None
        text = "$$"
        if v_i < 0:
            text += "v_i < 0; y_i = -1"
            retval = -1
        elif v_i > 0:
            text += "v_i > 0; y_i = 1"
            retval = 1
        elif v_i == 0:
            text += "v_i \\text{enak kot prej}; y_i = \\text{enako kot prej}"
            retval = y_before
        text += "$$"
        self.text_output.append(text)
        assert(retval is not None)
        return retval

    def y_i_0(self, v_i, y_before):
        retval = None
        text = "$$"
        if v_i < 0:
            text += "v_i < 0; y_i = 0"
            retval = 0
        elif v_i > 0:
            text += "v_i > 0; y_i = 1"
            retval = 1
        elif v_i == 0:
            text += "v_i \\text{enak kot prej}; y_i = \\text{enako kot prej}"
            retval = y_before
        text += "$$"
        self.text_output.append(text)
        return retval

    def v_i(self, i, y):
        def to_str(x):
            if x < 0:
                return "(%d)" % x
            else:
                return "%d" % x
        output = []
        izpis = "%s \cdot %s"
        str_vhod = map(to_str, y)
        str_w = map(to_str, self.weight[:, i])
        output = map(lambda x: izpis % x, zip(str_w, str_vhod))
        str_output = " + ".join(output)
        y = np.array(y)
        v = (self.weight[:, i].T * y).sum()
        if len(self.table) == 1:
            text = "$$v_i=\sum_{i=1}^{%d}w_{i j}y_i(t-1)$$" % self.number_of_weights
            self.text_output.append(text)
        text = "$$v_%d=" + str_output + " = %d$$"
        self.text_output.append(text % (i + 1, v))
        return v

    def run(self):
        truth_table = list(
            iproduct([0, 1], repeat=int(self.number_of_weights)))
        for index, input_row in enumerate(truth_table):
            self.text_output.append("<h3>Vrstica %d</h3>" % (index + 1, ))
            table_row = []
            table_row.extend(input_row)
            table_row.append(index)
            for i, input_y in enumerate(input_row):
                v_i = self.v_i(i, input_row)
                y_i = self.y_func(v_i, input_y)
                table_row.append(y_i)
            if self.function_type == 0:
                oznaka_bin = "".join(map(str, table_row[-self.number_of_weights:]))
                oznaka = int(oznaka_bin, 2)
                if oznaka == index:
                    oznaka = {'val': oznaka}
            else:
                oznaka = "??"
            table_row.append(oznaka)

            self.table.append(table_row)

if __name__ == "__main__":
    w = [[0, 1, -1],
         [1, 0, 1],
         [-1, 1, 0]]
    text_output = []

    hop = Hopfield(w, text_output)
    hop.run()
    for text in hop.table:
        print text
