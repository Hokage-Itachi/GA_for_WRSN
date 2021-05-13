class Node:
    def __init__(self, label, x, y, p, E_c):
        """

        :param label: name of node
        :param x: x- coordinate
        :param y: y- coordinate
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

    def __init__(self):
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

    def initialize(self, node_number):
        """
        Initialize population by backtracking.
        :param node_number
        :return: population
        """

        # backtracking
        def permutation(i, lst):
            for j in lst:
                if j not in ivd[:i]:
                    ivd[i] = j

                    if i == node_number - 1:
                        if len(population) == node_number ** 2:
                            return

                        population.append(Individual(ivd[0:node_number]))
                    else:
                        permutation(i + 1, lst)

        ivd = [i for i in range(1, node_number + 1)]
        population = []
        list_node = [i for i in range(1, node_number + 1)]

        permutation(0, list_node)

        return population

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

    def selection(self, population):
        """
        Select population_size / 2 best individual and choose random population-size / 2 individual left
        :param population
        :return: selected_population
        """
        pass

    def print_best_individual(self, population):
        """
        Print best individual of population
        :param population:
        :return: best_individual
        """

        pass


if __name__ == "__main__":
    wrsn = WRSN()
    wrsn.input_from_file("gr25_01_simulated.txt")

    # p = wrsn.initialize(4)
    # for i in p:
    #     print(i)
