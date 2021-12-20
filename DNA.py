# author: Parham Abdarzade
class DNA:

    def __init__(self, genes: []):
        self.genes = genes
        self.fitness = 0
        self.__evaluate_fitness()

    def __evaluate_fitness(self):

        fit_ratio = 0

        for i in range(len(self.genes) - 1):
            for j in range(i + 1, len(self.genes)):
                if self.__are_they_hit(i, self.genes[i], j, self.genes[j]):
                    fit_ratio += 1

        max_fit = (len(self.genes) * (len(self.genes) - 1)) / 2
        self.fitness = max_fit - fit_ratio

    @staticmethod
    def __are_they_hit(first_i, first_j, second_i, second_j) -> bool:
        if first_j == second_j:
            return True
        if abs(first_i - second_i) == abs(first_j - second_j):
            return True
        return False
