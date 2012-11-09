# -*- coding: utf-8 -*-
import math


class Neuron(object):

    def __init__(self, weight, text_output):
        self.weight = weight
        self.text_output = text_output

    def _perceptron(self, x, p=None):
        def to_str(x):
            if x < 0:
                return "(%0.1g)" % x
            else:
                return "%0.1g" % x
        output = []
        izpis = "%s*%s"
        str_vhod = map(to_str, x)
        str_w = map(to_str, self.weight)
        output = map(lambda x: izpis % x, zip(str_w, str_vhod))
        str_output = " + ".join(output)
        v = (self.weight.T * x).sum()
        v = float("%.3g" % v)
        out = "$$v^{(p)} = \sum_{i=0}^n w_i x_i$$"
        self.text_output.append(out)
        str_output = "$$v^{(%d)}=" + str_output + " = %.3g$$"
        str_output = str_output % (p, v)
        self.text_output.append(str_output)
        return v

    def get_d(self, d):
        return d


class LogisticNeuron(Neuron):

    def _output_string(self, x, y, p=None):
        str_output = "$$y^{(p)} = \\frac{1}{1+e^{-v}}$$"
        str_output_vals = "$$y^{(%d)} = \\frac{1}{1+e^{-%0.3g}} = %0.3g$$" % (p, x, y)
        self.text_output.append(str_output)
        self.text_output.append(str_output_vals)

    def get_output(self, x, p):
        v = self._perceptron(x, p)
        y = 1.0 / (1.0 + math.exp(-v))
        y = float("%.3g" % y)
        self._output_string(v, y, p)
        return y, v

    def get_derivation(self, y):
        text = "y^{(p)}(1-y^{(p)})"
        text_vals = "{y}(1-{y})"
        vals = y * (1 - y)
        return text, text_vals, vals


class TLU(Neuron):

    def _output_string(self, x, y, p=None):
        str_output = "$$y^{(p)} = v^{(p)}$$"
        str_output_vals = "$$y^{(%d)} = %0.3g$$" % (p, y)
        self.text_output.append(str_output)
        self.text_output.append(str_output_vals)

    def get_output(self, x, p):
        v = self._perceptron(x, p)
        y = v
        self._output_string(v, y, p)
        return y, v

    def get_d(self, d):
        d1 = []
        for index, _ in enumerate(d):
            if d[index][0] == 0:
                self.text_output.append(u"<h5>Popravljanje želenih izhodov ker TLU ni odvedljiv</h5>")
                self.text_output.append("$$d^{(%d)} = -1$$" % (index + 1,))
                d1.append([-1])
            else:
                d1.append([d[index][0]])
        return d1

    def get_derivation(self, y):
        return "", "", 1


if __name__ == "__main__":
    import numpy as np
    w = np.array([0.2, -0.3, -0.5, 0])
    x = np.array([[0, 0, 1],
                  [1, 0, 1]])
    bias = np.zeros((x.shape[0], 1)) - 1
    x = np.hstack((bias, x))
    text_output = []
    log = LogisticNeuron(w, text_output)
    #log.get_output(x[0])
    print log.get_output(x[0])
    for t in text_output:
        print t
