# -*- coding: utf-8 -*-
from Neuron import LogisticNeuron
from Neuron import TLU
import math
import numpy as np


def calc_weight_diff_cee(p, x, d, eta, y, text_output, neuron):
    text = "$$\Delta w_i^{(p)} = \eta \\times (y^{(p)} - d^{(p)}) \\times x_i^{(p)}$$"
    text_output.append(text)
    text = "$$\Delta w_{i}^{{({p})}} = {eta} \\times ({y} - {d}) \\times {x} = {rez: 0.3g}$$"
    delta_w = eta * (y - d[0]) * x
    for i in range(len(x)):
        text_output.append(text.format(
            p=p, i=i, eta=eta, y=y, d=d[0], x=x[i], rez=delta_w[i]))
        delta_w[i] = float("%0.3g" % delta_w[i])
    return delta_w


def calc_weight_diff_mse(p, x, d, eta, y, text_output, neuron):
    text_neuron, text_vals_neuron, vals_neuron = neuron.get_derivation(y)
    text = "$$\Delta w_i^{(p)} = \eta \\times " + text_neuron + "(d^{(p)}-y^{(p)}) \\times x_i^{(p)}$$"
    text_output.append(text)
    text = "$$\Delta w_{i}^{{({p})}} = {eta} \\times " + text_vals_neuron + \
           "  ({d} - {y}) \\times {x} = {rez: 0.3g}$$"
    delta_w = eta * vals_neuron * (d[0] - y) * x
    for i in range(len(x)):
        text_output.append(text.format(
            p=p, i=i, eta=eta, y=y, d=d[0], x=x[i], rez=delta_w[i]))
        delta_w[i] = float("%0.3g" % delta_w[i])
    return delta_w


def calc_ep_cee(p, d, y, text_output):
    text = "$$e^{(p)} = -d^{(p)}\ln(y^{(p)})-(1-d^{(p)})\ln(1-y^{(p)})$$"
    text_output.append(text)
    text = "$$e^{{({p})}} = -{d}\ln({y})-(1-{d})\ln(1-{y}) = {rez}$$"
    e_p = -d[0] * math.log(y) - (1 - d[0]) * math.log(1 - y)
    e_p = float("%0.3g" % e_p)
    text_output.append(text.format(p=p, d=d[0], y=y, rez=e_p))
    return e_p


def calc_ep_mse(p, d, y, text_output):
    text = "$$e^{(p)} = \\frac{1}{2} (d^{(p)}-v^{(p)})^2$$"
    text_output.append(text)
    text = "$$e^{{({p})}} = \\frac{{1}}{{2}} ({d}-{v})^2 = {rez}$$"
    e_p = 1 / 2.0 * (d[0] - y) ** 2
    e_p = float("%0.3g" % e_p)
    text_output.append(text.format(p=p, d=d[0], v=y, rez=e_p))
    return e_p


class DeltaLearning(object):

    def __init__(self, w, x, d, eta, text_output=[], epoch_learning=True,
                 neuron_type='logistic',
                 error_type='cee'):
        """Delta learning algorithm

        w - numpy array of weights
        x - numpy array input values
        d - true values
        eta - learning rate
        """
        self.w = np.array(w)
        x = np.array(x)
        bias = np.zeros((x.shape[0], 1)) - 1
        x = np.hstack((bias, x))
        self.x = x
        self.d = d
        self.eta = eta
        self.text_output = text_output
        self.epoch_learning = epoch_learning
        self.neurons = {'logistic': LogisticNeuron,
                        'tlu': TLU}
        self.errors = {'cee': calc_ep_cee,
                       'mse': calc_ep_mse,
                       }
        self.weights = {'cee': calc_weight_diff_cee,
                        'mse': calc_weight_diff_mse,
                        }
        if neuron_type in self.neurons:
            self.neuron = self.neurons[neuron_type](self.w, text_output)
            self.d = self.neuron.get_d(d)
            self.neuron_name = neuron_type
        else:
            raise Exception("Neuron type: %s doesn't exist!" % neuron_type)
        if error_type in self.errors:
            self.calc_ep = self.errors[error_type]
            self.error_type = error_type
            self.calc_weight_diff = self.weights[error_type]
        else:
            raise Exception("Error function: %s doesn't exist!" % error_type)
        self.table = []
        header = ["p"]
        self.number_of_weights = len(w)
        self.number_of_input_values = self.number_of_weights - 1  # - bias
        for i in range(1, self.number_of_input_values + 1):
            header.append("\(x_%d^{(p)}\)" % i)
        header.extend(["\(v^{(p)}\)", "\(y^{(p)}\)", "\(d^{(p)}\)"])
        for i in range(0, self.number_of_weights):
            header.append("\(\Delta w_%d^{(p)}\)" % i)
        for i in range(0, self.number_of_weights):
            if self.epoch_learning:
                header.append("\(\Delta w_%d\)" % i)
            else:
                header.append("\(w_%d\)" % i)
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
            self.text_output.append("<h3>Vzorec %d</h3>" % p)
            table_row = [p]
            table_row.extend(x_sample[1:])
            #print x_sample, d_sample
            self.text_output.append(u"<h4>Izračunamo aktivacijo \(v^{(p)}\) in izhod \(y^{(p)}\)</h4>")
# calculate activation v and output y
            y, v = self.neuron.get_output(x_sample, p)
            table_row.append(v)
            table_row.append(y)
            table_row.append(d_sample[0])
            #print y
            self.text_output.append(
                u"<h4>Izračuna popravke uteži \(\Delta w^{(p)}\)</h4>")
            delta_w = self.calc_weight_diff(p, x_sample, d_sample, self.eta,
                                    y, self.text_output, self.neuron)
            deltas_w.append(delta_w)
            table_row.extend(delta_w)
            if self.epoch_learning:
                table_row.extend(sum(deltas_w))
            else:
                new_w = self.w + delta_w
                table_row.extend(new_w)
                self.text_output.append(u"<p>Popravki uteži: \(\Delta w=\{%s\}\)</p>" %
                                        ", ".join(map(str, delta_w)))
                self.text_output.append(u"<p>Novi utežni vektor \(w=\{%s\}\)</p>" %
                                        ", ".join(map(str, new_w)))
                self.w = new_w
                self.neuron.weight = new_w

            #print delta_w
            self.text_output.append(
                u"<h4>Izračuna napako vzorca \(e^{(p)}\)</h4>")
            e_p = self.calc_ep(p, d_sample, y, self.text_output)
            table_row.append(e_p)
            e_ps.append(e_p)
            #print e_p
            self.table.append(table_row)
        self.text_output.append(
            u"<h4>Izračuna povprečno napako epohe \(E\)</h4>")
        text = "$$E = \\frac{1}{2}(e^{(1)}+e^{(2)})$$"
        self.text_output.append(text)
        E = 1 / 2.0 * sum(e_ps)
        text = "$$E = \\frac{1}{2}(%.3g + %.3g) = %.3g$$" % (
            e_ps[0], e_ps[1], E)
        self.text_output.append(text)
        if self.epoch_learning:
            delta_all_w = sum(deltas_w)
            new_w = self.w + delta_all_w
            self.text_output.append(u"<p>Skupni popravki uteži: \(\Delta w=\{%s\}\)</p>" %
                                    ", ".join(map(str, delta_all_w)))
            self.text_output.append(u"<p>Novi utežni vektor \(w=\{%s\}\)</p>" %
                                    ", ".join(map(str, new_w)))


        #break

if __name__ == "__main__":
    w = [0.2, -0.3, -0.5, 0]
    x = [[0, 0, 1],
         [1, 0, 1]]
    d = [[0],
        [1]]
    eta = 0.5
    #w = [0.1, -0.1, 0.5]
    #x = [[0.7, 0.4],
         #[0.3, 0.8]]
    #d = [[0],
         #[1]]
    delta = DeltaLearning(w, x, d, eta, epoch_learning=False,
                          neuron_type='tlu', error_type="mse")
    delta.run()
    for text in delta.text_output:
        print text
    print
