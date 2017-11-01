'''Coding Train NN-10.2 perceptron using fixed classification line'''
__author__ = 'Nicola Onofri'
__version__ = '1.0'

import numpy as np
import matplotlib.pyplot as plt


class Perceptron(object):
    '''Perceptron class'''
    learning_rate = 0.1  # learning rate

    def __init__(self):
        '''Class constructor'''
        self.weights = [np.random.randint(-1, 2)] * 2  # 2 random integers -1:1

    def guess(self, pts):
        '''Perceptron guessing test'''
        weighted_sum = np.sum([pts[i] * self.weights[i]
                               for i in range(0, len(pts))])  # weighted sum
        # sign function -> activator
        return np.sign(weighted_sum) if weighted_sum != 0 else 1

    def train(self, pts, target):
        '''Train the perceptron with pts for which there's a known answer'''
        guess = self.guess(pts)  # ask perceptron to guess
        error = target - guess  # compute error
        self.weights = [self.weights[i] + error * pts[i] * self.learning_rate
                        for i in range(0, len(pts))]  # tune weights according to error


def plot_dataset(pts, current_session, perceptron):
    '''Plot results of a perceptron training session'''
    #fig, ax = plt.subplots(2, sessions / 2, sharex=True, sharey=True)
    guessing_errors = 0

    fig = plt.figure('Training session results')
    ax = fig.add_subplot(1, 1, 1)
    for x, y in pts:
        if perceptron.guess((x, y)) != pts.get((x, y)):
            guessing_errors += 1
            ax.scatter(x, y, s=np.pi * (4**2),
                       color='yellow', edgecolors='black')
        else:
            ax.scatter(x, y, s=np.pi * (4**2),
                       color='blue', edgecolors='black')
    ax.plot([-1, 1], [-1, 1], 'k-', linewidth=1.3)
    ax.set_title('Training session #' + str(current_session))
    ax.grid()
    plt.show()  # a bit verbose, to be fixed
    # a plotting function shouldn't test and return values but who cares...
    return guessing_errors


def plot_guessing_errors(errors, generations):
    '''Plot guessing mistakes for each training session'''
    fig = plt.figure('Errors')
    ax = fig.add_subplot(1, 1, 1)
    ax.plot(range(0, generations), errors, 'k-', marker='o')
    ax.set_xlabel('$generation$')
    ax.set_ylabel('$errors$')
    ax.set_title('$Errors$')
    ax.grid()
    plt.show()


def main():
    '''Create and train a perceptron, then plot its results'''
    # Creating training dataset
    dataset_dim = 100
    generations = 5  # keep this number small otherwise prepare yourself to a long series of plots
    pts = {}  # {(x,y):val}
    for _ in range(0, dataset_dim):
        x = float(np.random.random(1) * 2 - 1)  # rnd -1:1
        y = float(np.random.random(1) * 2 - 1)  # rnd -1:1
        val = 1 if x > y else -1  # supervised learning strategy
        pts[(x, y)] = val

    p = Perceptron()
    errors = []

    # training and error evaluation
    for gen in range(0, generations):
        err = 0
        for x, y in pts:
            p.train((x, y), pts.get((x, y)))  # training for each point
        err = plot_dataset(pts, gen, p)
        print 'Errors @ generation ' + str(gen) + ': ' + str(err)
        errors.append(err)
    plot_guessing_errors(errors, generations)


if __name__ == '__main__':
    main()
