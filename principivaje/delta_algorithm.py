from Neuron import LogisticNeuron
import math

def adjust_weight(p, x, d, eta, y, text_output):
    text = "$$\Delta w_i^{(p)} = \eta \\times (y^{(p)} - d^{(p)}) \\times x_i^{(p)}"
    text_output.append(text)
    text = "$$\Delta w_{i}^{{({p})}} = {eta} \\times ({y} - {d}) \\times {x} = {rez: 0.3g}"
    delta_w = eta * (y-d) * x
    for i in range(len(x)):
        text_output.append(text.format(p=p, i=i, eta=eta, y=y, d=d[0], x=x[i], rez=delta_w[i]))
        delta_w[i] = float("%0.3g" % delta_w[i])
    return delta_w

def calc_ep(p, d, y, text_output):
    text = "$$e^{(p)} = -d^{(p)}\ln(y^{(p)})-(1-d^{(p)})ln(1-y^{(p)})$$"
    text_output.append(text)
    text = "$$e^{{({p})}} = -{d}\ln({y})-(1-{d})ln(1-{y}) = {rez}$$"
    e_p = -d * math.log(y)-(1-d[0])*math.log(1-y)
    e_p = float("%0.3g" % e_p)
    text_output.append(text.format(p=p, d=d[0], y=y, rez=e_p))
    return e_p




class DeltaLearning(object):

    def __init__(self, w, x, d, eta, text_output=[], epoch_learning=True,
                 neuron_type = 'logistic'):
        """Delta learning algorithm

        w - numpy array of weights
        x - numpy array input values
        d - true values
        eta - learning rate
        """
        self.w = w
        self.x = x
        self.d = d
        self.eta = eta
        self.text_output = text_output
        self.epoch_learning = epoch_learning
        self.neurons = {'logistic':LogisticNeuron}
        if neuron_type in self.neurons:
            self.neuron = self.neurons[neuron_type](w, text_output)
        else:
            raise Exception("Neuron type: %s doesn't exist!" % neuron_type)
        self.table = []
        header = ["p"]
        number_of_weights = len(w)
        number_of_input_values = number_of_weights - 1# - bias
        for i in range(1, number_of_input_values):
            header.append("\(x_%d^{(p)}\)" % i)
        header.extend(["\(v^{(p)}\)","\(y^{(p)}\)", "\(d^{(p)}\)"])
        for i in range(0, number_of_weights):
            header.append("\(\delta_%d^{(p)}\)" % i)
        for i in range(0, number_of_weights):
            header.append("\(\delta_%d\)" % i)
        header.append("\(e^{(p)}\)")
        self.table.append(header)

    def run(self):
        deltas_w = []
        e_ps = []
        #for head in chain(["p"],
                #header.append("\(x_%d^{(p)}\)" % i)
# for each learning sample
        for p, x_sample, d_sample in zip(range(1, len(self.x) + 1),
                                         self.x, self.d):
            print x_sample, d_sample
# calculate activation v and output y
            y = self.neuron.get_output(x_sample)
            print y
            delta_w = adjust_weight(p, x_sample, d_sample, self.eta,
                                    y, self.text_output)
            deltas_w.append(delta_w)
            print delta_w
            e_p = calc_ep(p, d_sample, y, self.text_output)
            e_ps.append(e_p)
            print e_p
        text = "$$E = \\frac{1}{2}(e^{(1)}+e^{(2)})$$"
        text_output.append(text)
        E = 1 / 2.0 * sum(e_ps)
        text = "$$E = \\frac{1}{2}(%.3g + %.3g) = %.3g" % (e_ps[0], e_ps[1], E)
        text_output.append(text)
        print sum(deltas_w)

        #break

if __name__ == "__main__":
    import numpy as np
    #w = np.array([0.2, -0.3, -0.5, 0])
    #x = np.array([[0, 0, 1],
                  #[1, 0, 1]])
    #d = np.array([[0],
                  #[1]])
    eta = 0.5
    w = np.array([0.1, -0.1, 0.5])
    x = np.array([[0.7, 0.4],
                  [0.3, 0.8]])
    d = np.array([[0],
                  [1]])
    bias = np.zeros((x.shape[0], 1)) - 1
    x = np.hstack((bias, x))
    text_output = []
    delta = DeltaLearning(w, x, d, eta, text_output, epoch_learning=True)
    delta.run()
    for text in text_output:
        print text
    print
