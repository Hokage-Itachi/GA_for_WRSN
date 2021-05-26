import math
import random


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
    def __init__(self, chromosome, fitness=0.0):
        self.chromosome = chromosome
        self.fitness = fitness

    def __repr__(self):
        return "[Idv:" + str(self.chromosome) + ", fitness= " + str(self.fitness) + "]"


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
        # total time for a cycle
        self.total_time = 20000
        # speed of MC. Calculation Unit(m/s)
        self.v = 5

        self.base_station = None
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
        self.base_station = Node("0", float(lines[0].split()[0]), float(lines[0].split()[1]), 0, 0)
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
        Initialize population by shuffle init list

        """

        node_num = len(self.nodes)
        init_chromosome = [i for i in self.nodes]

        while len(self.population) < node_num ** 2:
            copy_chromosome = init_chromosome[:]

            random.shuffle(copy_chromosome)
            if copy_chromosome not in self.population:
                fitness = self.calc_fitness(copy_chromosome)
                self.population.append(Individual(copy_chromosome, fitness))

        # print("here")

    def crossover(self, dad, mom):
        """
        Crossover dad and mom to create two children.
        :param dad:
        :param mom:
        :return: child_1, child_2
        """

        child_1 = self.ox_crossover(dad.chromosome, mom.chromosome)
        fitness_1 = self.calc_fitness(child_1)
        child_2 = self.ox_crossover(mom.chromosome, dad.chromosome)
        fitness_2 = self.calc_fitness(child_2)
        return Individual(child_1, fitness_1), Individual(child_2, fitness_2)

    def ox_crossover(self, dad, mom):
        """
        Create child using Order Crossover
        :param dad: chromosome dad
        :param mom: chromosome mom
        :return: child chromosome
        """
        r = random.Random()
        n = len(dad)
        p = r.randint(0, n)
        q = r.randint(0, n)

        while q == p:
            q = r.randint(0, n)
        if p > q:
            p, q = q, p

        left_segment = [0 for i in range(0, n)]
        center_segment = [dad[i] for i in range(p, q)]
        right_segment = [0 for i in range(0, n)]

        i = 0
        for item in mom:
            if not item in center_segment:
                if i < p:
                    left_segment[i] = item
                    i += 1
                    continue
                elif i == p:
                    i = q
                    right_segment[i] = item
                    i += 1
                    continue
                if i > q:
                    right_segment[i] = item
                    i += 1
                    continue
                if i == n:
                    break

        child = left_segment[0:p] + center_segment[:] + right_segment[q:n]
        return child

    def mutation(self, individual):
        """
        Mutation by exchange two gene of individual
        :param individual:
        :return: new_individual
        """

        chromosome = individual.chromosome
        fitness = individual.fitness
        m = random.Random().randint(0, len(chromosome) - 1)

        n = random.Random().randint(0, len(chromosome) - 1)

        chromosome[m], chromosome[n] = chromosome[n], chromosome[m]

        return Individual(chromosome, fitness)

    def selection(self):
        """
        Select population_size / 2 best individual and choose random population-size / 2 individual left
        :return: selected_population
        """
        k = len(self.population) // 4
        sorted(self.population, key=lambda individual: individual.fitness, reverse=True)
        selected_population = self.population[0:k]
        n = len(selected_population)
        while n < 2 * k:
            i = random.Random().randint(k, len(self.population) - 1)
            idv = self.population[i]
            selected_population.append(idv)
            self.population.remove(idv)

            n += 1

        self.population = selected_population[:]

    def apply_operator(self):
        copied_population = self.population[:]

        while len(copied_population) > 1:
            n = len(copied_population) - 1
            k = random.Random().randint(0, n)
            h = n - k
            if h == k:
                h -= 1

            dad = copied_population[k]
            mom = copied_population[h]

            child_1, child_2 = self.crossover(dad, mom)

            child_1 = self.mutation(child_1)
            child_2 = self.mutation(child_2)
            try:
                copied_population.remove(dad)
                copied_population.remove(mom)
            except ValueError as e:
                print(k, h)
                print(len(copied_population))

            self.population.append(child_1)
            self.population.append(child_2)

    def calc_fitness(self, chromosome):
        t_tsp = self.euclid_distance(self.base_station, chromosome[0]) / self.v
        total_charge_time = 0

        for i in range(len(chromosome) - 1):
            total_charge_time += self.get_time_charge(chromosome[i], t_tsp + total_charge_time)
            t_tsp += self.euclid_distance(chromosome[i], chromosome[i + 1]) / self.v
        t_tsp += self.euclid_distance(chromosome[-1], self.base_station) / self.v

        return (self.total_time - t_tsp - total_charge_time) / self.total_time

    def euclid_distance(self, from_node, to_node):

        return math.sqrt((from_node.x - to_node.x) ** 2 + (from_node.y - to_node.y) ** 2)

    def get_time_charge(self, node, previous_time):
        needed_charge_energy = node.p * previous_time

        time_charge = needed_charge_energy / self.U
        return time_charge


if __name__ == "__main__":
    wrsn = WRSN("gr25_01_simulated.txt")

    wrsn.initialize()
    dad = wrsn.population[0]
    mom = wrsn.population[1]

    # c1, c2 = wrsn.crossover(dad, mom)
    # print(c1)
    # print(c2)
    for k in range(100):
        wrsn.apply_operator()
        wrsn.selection()

    print(wrsn.population[0])
