# -*- coding: utf-8 -*-
import numpy as np
from itertools import product as iproduct


class Hopfield(object):

    def __init__(self, function_type=0, text_output=[]):
        """Delta learning algorithm

        w - numpy array of weights
        """
        self.text_output = text_output
        self.weight = None
        self.function_type = function_type
        if function_type == 0:
            self.y_func = self.y_i_0
        elif function_type == 1:
            self.y_func = self.y_i_1
        else:
            raise Exception("Invalid function: %d!" % (function_type,))
        self.table = []

    @property
    def weight_matrix(self):
        """Weight matrix property"""
        return self.weight

    @weight_matrix.setter
    def weight_matrix(self, value):
        #:TODO error checking
        self.weight = np.array(value)

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

    def v_i(self, i, j, y):
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
# this is basically a matrix multiplication
# take one row of inputs and multiply it with weights in column i
# and we get rezult of at v_i in the same row as row of inputs
        v = (self.weight[:, i].T * y).sum()
        if len(self.table) == 1:
            text = "$$v_i=\sum_{i=1}^{%d}w_{i j}y_i(t-1)$$" % self.number_of_weights
            self.text_output.append(text)
        w_y = "w_{{{r},{j}}} y_{r}(t-1)"
        long_part = []
        for r in range(self.number_of_weights):
            long_part.append(w_y.format(r=r + 1,j=i + 1))
        text_long = "$$v_%d = " + " + ".join(long_part) + "$$"
        self.text_output.append(text_long % (i + 1, ))
        text = "$$v_%d=" + str_output + " = %d$$"
        self.text_output.append(text % (i + 1, v))
        return v

    def get_stable_states(self):
        if self.weight is None:
            raise Exception("Weight matrix is empty!")
        self.text_output.append(
            u"<h2>Sinhrono pridobivanje stabilnih stanj</h2>")
        if self.function_type == 0:
            self.text_output.append(r"$$y =  \left\{\begin{matrix} 0 & \mbox {if } v < 0, \\ 1 & \mbox{if } v > 0, \\ \text{enako kot prej} & \mbox{if } v=0\end{matrix}\right.$$")
        elif self.function_type == 1:
            self.text_output.append(r"$$y =  \left\{\begin{matrix} -1 & \mbox {if } v < 0, \\ +1 & \mbox{if } v > 0, \\ \text{enako kot prej} & \mbox{if } v=0\end{matrix}\right.$$")
            self.text_output.append(u'<span class="label label-warning">Opozorilo</span>Ta funkcija je še v beta stanju. Nevem namreč kako računat oznake</p>')
        self.number_of_weights = len(self.weight)
        weights_label = ["\(y_%d\)" % i for i in range(1,
                                                       self.number_of_weights + 1)]
        header = weights_label + ["Oznaka"] + weights_label + ["Oznaka"]
        self.table.append(header)
        truth_table = list(
            iproduct([0, 1], repeat=int(self.number_of_weights)))
        for index, input_row in enumerate(truth_table):
            self.text_output.append("<h3>Vrstica %d</h3>" % (index + 1, ))
            table_row = []
            table_row.extend(input_row)
            table_row.append(index)
            for i, input_y in enumerate(input_row):
                v_i = self.v_i(i, index + 1, input_row)
                y_i = self.y_func(v_i, input_y)
                table_row.append(y_i)
            if self.function_type == 0:
                oznaka_bin = "".join(
                    map(str, table_row[-self.number_of_weights:]))
                oznaka = int(oznaka_bin, 2)
                if oznaka == index:
                    oznaka = {'val': oznaka}
            else:
                oznaka = "??"
            table_row.append(oznaka)

            self.table.append(table_row)

    def convert_inputs(self, inputs):
        text = "$$y_{i,j} = \mathop{\mathrm{sgn}}(x_{i,j} - 0.5)$$"
        self.text_output.append(text)
        text = "$${x}_{i}=({xes}) = ({xvals})$$"
        y_ij = np.sign(inputs - 0.5)
        for p, one_input, one_output in zip(xrange(1,len(inputs) + 1), inputs, y_ij):
            xes = ",".join(["x_{%d,%d}" % (p,i + 1) for i in range(self.N)])
            xvals = ",".join(map(str,one_input))
            self.text_output.append(text.format(x="x", xes=xes, i=p,xvals=xvals))
            yes = ",".join(["y_{%d,%d}" % (p,i + 1) for i in range(self.N)])
            yvals = ",".join(map(lambda x: str(int(x)),one_output))
            self.text_output.append(text.format(x="y", xes=yes, i=p, xvals=yvals))
        return y_ij

    def learn(self, inputs):
        self.text_output.append(u"<h2>Učenje Hopfieldove mreže z Hebbovim učnim pravilom</h2>")

        inputs = np.array(inputs)
        self.N = inputs.shape[1]
        p = inputs.shape[0]
        converted_inputs = self.convert_inputs(inputs)
        self.weight = np.zeros((self.N, self.N))
        text = "$$w_{{{i},{j}}}=\\frac{{1}}{{{N}}}\sum_{{k=1}}^{p}y_{{k,{i}}}y_{{k,{j}}}$$"
        text_vals = "$$w_{{{i},{j}}}=\\frac{{1}}{{{N}}} ("
        text_bet_vals = "y_{{{k},{i}}} \cdot y_{{{k},{j}}}"
        text_cdot = "{y1:0g} \cdot {y2:0g}"
        text_0 = "$$w_{{{i},{j}}} = 0$$"
        for j in xrange(0, self.N):
            for i in xrange(j, self.N):
                if i != j:
                    weight = 0
                    text_out = []
                    text_vals_out = []
                    for k, one_input in enumerate(converted_inputs):
                        weight += one_input[i] * one_input[j]
                        text_out.append(text_bet_vals.format(k=k + 1, i=i + 1, j=j + 1))
                        text_vals_out.append(text_cdot.format(y1=one_input[i], y2=one_input[j]))

                    text_vals_start = text_vals.format(i=i + 1, j=j + 1, N=self.N)
                    text_write = text_vals_start + " + ".join(text_out) + ")$$"
                    text_write_values = text_vals_start + " + ".join(text_vals_out) + ") = {rez:0g}$$".format(rez=weight)
                    self.text_output.append(text.format(i=i + 1, j=j + 1, N=self.N, p=p))
                    self.text_output.append(text_write)
                    self.text_output.append(text_write_values)
                    self.weight[i,j] = weight
                    self.weight[j,i] = weight
                else:
                    self.text_output.append(text_0.format(i=i + 1, j=j + 1))

        self.pretty_weight = self.weight.copy()
        self.text_output.append(u"<h4>Izračunano je za levo spodnjo diagonalo. Matrika je simetrična</h4>")
        weight_text = "$$W = \\frac{1}{%d} \\begin{bmatrix} " % (self.N,)
        weight_lines = []
        for line in self.weight:
            str_line = " & ".join(map(lambda x: str(int(x)), line))
            weight_lines.append(str_line)
        weight_text += "\\\\".join(weight_lines) + "\\end{bmatrix}$$"
        self.text_output.append(weight_text)

        self.weight *= 1.0/self.N


if __name__ == "__main__":
    w = [[0, 1, -1],
         [1, 0, 1],
         [-1, 1, 0]]
    vhod = [[0, 0, 1, 1],
            [0, 1, 0, 1]]
    text_output = []

    hop = Hopfield(text_output=text_output)
    hop.learn(vhod)
    print hop.weight_matrix
    print hop.pretty_weight
    #hop.weight_matrix = w
    #hop.run()
    for text in hop.text_output:
        print text
