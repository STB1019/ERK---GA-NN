'''Genetic Algorithm template in Python'''

import timeit
import string
import random as rnd
import numpy as np


class DNA(object):
    '''DNA class'''

    def __init__(self, target, genes=''):
        '''DNA class constructor'''
        # in this particular case DNA is a string and genes are characters that form that string
        self.target = target
        self.genes = random_string(
            len(self.target), symbol_set=string.letters + ' ') if genes == '' else genes

    def __repr__(self):
        return 'DNA sequence: ' + str(self.genes)

    def DNA_fitness(self):
        '''Evaluate fitness score for this DNA sequence'''
        # In this case fitness_score is incremented if the i-th gene (in this case the i-th letter)
        # corresponds to the i-th character of the target string
        fitness_score = 0
        for i in range(0, len(self.genes)):
            fitness_score += 1 if self.target[i] == self.genes[i] else 0
        return fitness_score


class Population(object):
    '''Population class: simulates a population of DNAs'''
    population = []

    def __init__(self, max_population, target, mutation_rate):
        '''Population class constructor '''
        for _ in range(0, max_population):
            # calling default DNA constructor
            d = DNA(target)
            self.population.append(d)
        self.target = target
        self.max_population = max_population
        self.mutation_rate = mutation_rate

    def population_fitness(self, target):
        '''Calculate fitness for each member in the given population'''
        fitness_scores = {}  # {DNA:score}
        max_fitness_score = 0
        max_seq_fitness = ''

        for d in self.population:
            score = d.DNA_fitness()

            if score > max_fitness_score:
                if score == len(target):  # solution has been found
                    del fitness_scores  # clear dictionary
                    return {d: len(target)}  # return current sequence
                else:
                    max_fitness_score = score
                    max_seq_fitness = d
            fitness_scores[d] = score  # update dict

        print 'Max fitness element: ' + str(max_seq_fitness) + ' - score: ' + str(max_fitness_score)
        return fitness_scores

    def mating_pool_classic(self, fitness_scores):
        '''Each DNA has probability to be picked from the mating pool directly proportional to its fitness score '''
        pool = []
        # Extremely slow, bottleneck of the entire algorithm + extreme use of memory
        # Alternative solution: Monte Carlo Method
        for p, score in fitness_scores.iteritems():
            for i in xrange(0, score):
                pool.append(p)
        return pool

    def reproduce_split(self, d1, d2):  # old solution
        '''Create a new DNA given the 2 parents' DNAs taking 50% genetic
        information from each one + consider mutation rate'''
        child = d1.genes[:len(d1.genes) / 2] + d2.genes[len(d2.genes) / 2:]
        mut_child = []
        for x in child:
            if np.random.random() > self.mutation_rate:
                mut_child.append(x)
            else:
                # perform mutation
                mut_child.append(random_string(
                    symbol_set=string.letters + ' '))
        dc = DNA(self.target, mut_child)
        return dc

    def reproduce_uniform(self, d1, d2):  # agb91 solution
        '''Create a new DNA given the 2 parents' DNAs by taking father or mother genes uniformely'''
        child = []
        mut_child = []
        for i in range(0, len(d1.genes)):  # slow for loop, can it be replaced with list comprehension?
            x = d1.genes[i] if np.random.random() < 0.5 else d2.genes[i]
            child.append(x)
        for x in child:
            if np.random.random() > self.mutation_rate:
                mut_child.append(x)
            else: #perform mutation
                mut_child.append(random_string(symbol_set=string.letters+' '))
        dc = DNA(self.target, mut_child)
        return dc

    def natural_selection(self):
        '''Perform natural selection on the population: members
        with higher fitness score have higher probability of being select for reproduction'''
        fitness_scores = self.population_fitness(self.target)
        if len(fitness_scores) == 1:  # optimal solution found!
            return str(fitness_scores.keys()[0])

        mating_pool = self.mating_pool_classic(fitness_scores)
        print 'MP size: ' + str(len(mating_pool))

        new_generation = []

        # standard solution
        # for x in range(0, self.max_population):
        #     new_generation.append(self.reproduce_split(
        #         rnd.choice(mating_pool), rnd.choice(mating_pool)))

        # agb91 solution
        for x in range(0, self.max_population):
            new_generation.append(self.reproduce_uniform(
                rnd.choice(mating_pool), rnd.choice(mating_pool)))

        # clear population and replace it
        self.population = new_generation
        return None


def random_string(length=1, symbol_set=string.letters + string.digits):
    '''Utility random string generator, for random DNA sequence generation'''
    return str(''.join(rnd.choice(str(symbol_set)) for _ in range(0, length)))


def main():
    '''Initializes population, breeds, evolves until it reaches the given target'''
    target = 'To be or not to be'  # str.letters + ' ': pay attention to this attribute otherwise your computer will explode
    dim = 500
    mutation_rate = 0.01
    generation = 0

    p = Population(dim, target, mutation_rate)  # population __init__
    while True:
        res = p.natural_selection()
        if res != None:
            print 'Optimal solution found!'
            break

        print 'Generation: ' + str(generation) + ':\t',
        generation += 1


if __name__ == '__main__':
    start_time = timeit.default_timer()
    main()
    print 'Execution time: ' + str(timeit.default_timer() - start_time)
