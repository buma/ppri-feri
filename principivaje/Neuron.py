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
