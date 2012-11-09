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





def delta(w, x, d, eta, text_output=[], epoch_learning=True):
    """Delta learning algorithm

    w - numpy array of weights
    x - input values
    d - right values
    eta - learning rate
    """
    log_neuron = LogisticNeuron(w, text_output)
    deltas_w = []
    e_ps = []
# for each learning sample
    for p, x_sample, d_sample in zip(range(1, len(x) + 1), x, d):
        print x_sample, d_sample
# calculate activation v and output y
        y = log_neuron.get_output(x_sample)
        print y
        delta_w = adjust_weight(p, x_sample, d_sample, eta, y, text_output)
        deltas_w.append(delta_w)
        print delta_w
        e_p = calc_ep(p, d_sample, y, text_output)
        e_ps.append(e_p)
        print e_p
    text = "$$E = \\frac{1}{2}(e^{(1)}+e^{(2)})$$"
    text_output.append(text)
    E = 1/2.0 * sum(e_ps)
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
    print delta(w, x, d, eta, text_output, epoch_learning=True)
    for text in text_output:
        print text
