import itertools
import sys


class Node:
    def __init__(self, label, x, y, p, E_c):
        """

        :param label: name of node
        :param x: x-coordinate
        :param y: y-coordinate
        :param p: power consumption
        :param E_c: current energy
        """
        self.label = label
        self.x = x
        self.y = y
        self.p = p
        self.E_c = E_c

    def __repr__(self):
        return self.label


class Individual:
    def __init__(self, path, fitness=0):
        self.path = path
        self.fitness = fitness

    def __repr__(self):
        return "[Idv:" + str(self.path) + ", fitness= " + str(self.fitness) + "]"


class WRSN:
    path = "small-net/grid/base_station_(250.0, 250.0)/"

    def __init__(self, filename):
        """
        Create network with data from file
        :param filename: file to read data
        """
        # list node of network
        self.nodes = []
        # maximum energy of each node. Calculation Unit(J)
        self.E_max = 10800
        # minimum energy of each node. Calculation Unit(J)
        self.E_min = 540
        # Charging energy of mobile charger. Calculation Unit(J)
        self.E_MC = 108000
        # Moving power of mobile charger. Calculation Unit(J/s)
        self.P_M = 1
        # Charging power of mobile charger. Calculation Unit(J/s)
        self.U = 5

        self.population = []

        self.input_from_file(filename)

    def input_from_file(self, filename):
        """
        Read input from file
        :param filename:
        :return:
        """

        f = open(self.path + filename, "r", encoding="utf-8")

        lines = f.readlines()
        n = len(lines)
        for i in range(1, n):
            line = lines[i]
            # print(lines)
            params = line.split()
            # print(params)

            x = float(params[0])
            y = float(params[1])
            p = float(params[2])
            e_c = float(params[3])

            node = Node(str(i), x, y, p, e_c)

            self.nodes.append(node)

    def initialize(self):
        """
        Initialize population by backtracking.
        :return: population
        """

        # backtracking

        node_num = len(self.nodes)
        cycle = [i for i in self.nodes]

        p = itertools.permutations(cycle)
        for i in range(node_num ** 2):
            self.population.append(Individual(p.__next__()))
        # print("here")

    def crossover(self, dad, mom):
        """
        Crossover dad and mom to create two children.
        :param dad:
        :param mom:
        :return: child_1, child_2
        """
        pass

    def mutation(self, individual):
        """
        Mutation by exchange two gene of individual
        :param individual:
        :return: new_individual
        """
        pass

    def selection(self):
        """
        Select population_size / 2 best individual and choose random population-size / 2 individual left
        :param population
        :return: selected_population
        """
        pass

    def print_best_individual(self):
        """
        Print best individual of population
        :return: best_individual
        """

        pass


if __name__ == "__main__":
    wrsn = WRSN("gr25_01_simulated.txt")

    wrsn.initialize()


