# author: Parham Abdarzade
import random

from DNA import DNA


class Population:

    def __init__(self, pop_size, mutation_rate, queen_number, selection_factor):
        self.pop_size = pop_size
        self.queen_number = queen_number
        self.fit_mean = 0.0
        self.max_fit = queen_number * (queen_number - 1) / 2
        self.mutation_rate = mutation_rate
        self.pop: [DNA] = self.__generate_first_generation()
        self.selection_factor = selection_factor

    def __generate_first_generation(self) -> [DNA]:
        pop = []
        fit_sum = 0
        for i in range(self.pop_size):
            pop.append(self.__generate_dna())
            fit_sum += pop[i].fitness

        self.fit_mean = ((fit_sum / self.pop_size) / self.max_fit) * 100
        print("First Fit Average :", self.fit_mean)
        return pop

    def __generate_dna(self) -> DNA:
        genes = [random.randrange(self.queen_number) for _ in range(self.queen_number)]
        return DNA(genes)

    def is_solution_has_been_found(self) -> bool:
        for i in self.pop:
            if i.fitness == self.max_fit:
                self.__print_solution(i)
                return True

        return False

    @staticmethod
    def __print_solution(sol: DNA):
        print(" \n \nFounded Solution:")
        rows, cols = (len(sol.genes), len(sol.genes))
        n_queen = [[0 for i in range(cols)] for j in range(rows)]

        for i in range(len(sol.genes)):
            n_queen[i][sol.genes[i]] = 1

        for i in n_queen:
            print(i)

    @staticmethod
    def __print_best_fit(dna):
        if len(dna.genes) < 50:
            print("Best Fit:")
            rows, cols = (len(dna.genes), len(dna.genes))
            n_queen = [[0 for i in range(cols)] for j in range(rows)]

            for i in range(len(dna.genes)):
                n_queen[i][dna.genes[i]] = 1

            for i in n_queen:
                print(i)

    def natural_selection(self):
        next_gen = []
        fit_sum = 0
        self.__sort_pop()

        for i in range(int(self.pop_size / 2)):
            parent_a = self.pop[self.__select_parent()]
            parent_b = self.pop[self.__select_parent()]
            children = self.__crossover(parent_a, parent_b)
            next_gen.append(children[0])
            next_gen.append(children[1])
            fit_sum += next_gen[i * 2].fitness
            fit_sum += next_gen[(i * 2) + 1].fitness

        self.fit_mean = ((fit_sum / self.pop_size) / self.max_fit) * 100
        print("Fit Average :", self.fit_mean)
        self.pop = next_gen

    def __sort_pop(self):
        self.pop.sort(key=lambda x: x.fitness, reverse=True)

    def __select_parent(self) -> int:
        r = random.uniform(0, 1)
        return int(self.pop_size * (pow(r, self.selection_factor)))

    def __crossover(self, parent_a: DNA, parent_b: DNA) -> [DNA]:
        child_one_gene = []
        child_two_gene = []

        point_one = random.randrange(self.queen_number)
        for i in range(point_one):
            child_one_gene.append(parent_a.genes[i])
            child_two_gene.append(parent_b.genes[i])

        for i in range(point_one, self.queen_number):
            child_one_gene.append(parent_b.genes[i])
            child_two_gene.append(parent_a.genes[i])

        return [DNA(self.__mutate(child_one_gene)), DNA(self.__mutate(child_two_gene))]

    def __mutate(self, genes) -> []:
        pos = random.uniform(0, 1)
        if pos < self.mutation_rate:
            r_index = random.randrange(self.queen_number)
            r_value = random.randrange(self.queen_number)
            genes[r_index] = r_value

        return genes
