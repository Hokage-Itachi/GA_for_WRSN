class Node:
    def __init__(self, label, x, y, p):
        self.label = label
        self.x = x
        self.y = y
        self.p = p

    def __repr__(self):
        return self.label


class Individual:
    def __init__(self, path, fitness=0):
        self.path = path
        self.fitness = fitness

    def __repr__(self):
        return "[Idv:" + str(self.path) + ", fitness= " + str(self.fitness) + "]"


class WRSN:

    def input_from_file(self, filename):
        """
        Read input from file
        :param filename:
        :return:
        """
        pass

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

    # p = wrsn.initialize(4)
    # for i in p:
    #     print(i)
