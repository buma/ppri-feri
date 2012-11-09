import math


class Neuron(object):

    def __init__(self, weight, text_output):
        self.weight = weight
        self.text_output = text_output

    def _perceptron(self, x):
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
        str_output = "$$v=" + str_output + " = %.03g$$" % v
        self.text_output.append(str_output)
        return v


class LogisticNeuron(Neuron):

    def _output_string(self, x, y):
        str_output = "$$y = \\frac{1}{1+\e^{-x}}$$"
        str_output_vals = "$$y = \\frac{1}{1+\e^{-%0.3g}} = %0.3g$$" % (x, y)
        self.text_output.append(str_output)
        self.text_output.append(str_output_vals)

    def get_output(self, x):
        v = self._perceptron(x)
        y = 1.0 / (1.0 + math.exp(-v))
        self._output_string(v, y)
        return y

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
