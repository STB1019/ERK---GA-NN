'''Coding Train perceptron example in Python'''
__author__ = 'Nicola Onofri'
__version__ = '1.0'

import numpy as np
import matplotlib.pyplot as plt


class Perceptron(object):
    '''Perceptron class'''
    learning_rate = 0.1  # learning rate

    def __init__(self):
        '''Class constructor'''
        self.weights = [np.random.randint(-1, 2)] * 2  # 2 dimensions

    def guess(self, input):
        '''Perceptron guessing test'''
        weighted_sum = np.sum([input[i] * self.weights[i]
                               for i in range(0, len(input))])  # weighted sum
        # sign function -> activator
        return np.sign(weighted_sum) if weighted_sum != 0 else 1

    def train(self, input, target):
        '''Train the perceptron with inputs for which there's a known answer'''
        guess = self.guess(input)  # ask perceptron to guess
        error = target - guess  # compute error
        self.weights = [self.weights[i] + error * input[i] * self.learning_rate
                        for i in range(0, len(input))]  # tune weights according to error


def plot_dataset(pts, override=True, show=False):
    '''Plot results of a single training session '''
    if not override:  # expecting result
        for x, y in pts:
            if pts.get((x, y)) == 1:
                plt.scatter(x, y, s=np.pi * (3**2),
                            color='black', edgecolors='black')
            else:
                plt.scatter(x, y, s=np.pi * (3**2),
                            color='white', edgecolors='black')
        plt.plot([0, 2], [0, 2], 'k-', linewidth=1.3)

    else:  # training session
        pass
    if show:
        plt.grid()
        plt.show()


def plot_guessing_errors(errors, generations):
    fig = plt.figure('Errors')
    ax = fig.add_subplot(1, 1, 1)
    # ax.scatter(range(0, generations), errors, s=np.pi *
    #            (3**2), color='white', edgecolors='black')
    ax.plot(range(0, generations), errors, 'k-', marker='o')
    ax.set_xlabel('$generation$')
    ax.set_ylabel('$errors$')
    ax.set_title('$Errors$')
    ax.grid()
    plt.show()


def main():
    '''Create and train a perceptron, then plot its results'''
    # Creating training dataset
    dataset_dim = 1000
    pts = {}  # {(x,y):val}
    for _ in range(0, dataset_dim):
        x = float(np.random.random(1) * 2)
        y = float(np.random.random(1) * 2)
        val = 1 if x > y else -1  # supervised learning strategy
        pts[(x, y)] = val

    p = Perceptron()
    errors = []

    # training and error evaluation
    for gen in range(0, 10):
        err = 0
        for x, y in pts:
            p.train((x, y), pts.get((x, y)))
            # evaluate improvements
            if p.guess((x, y)) != pts.get((x, y)):
                err += 1
        print 'Errors @ generation ' + str(gen) + ': ' + str(err)
        errors.append(err)
    plot_guessing_errors(errors, 10)


if __name__ == '__main__':
    main()
