import random
import math

from MyTSP import MyTSP
import numpy as np


class MGA:
    def __init__(self, population_size, cross_rate, mutation_rate, problem: dict):
        """
        dna_size : 一個人有幾個DNA
        population_size : 一個世代有幾個人
        cross_rate : 繁殖時每項DNA的交換機率
        mutation_rate : 每項DNA的變異機率
        """
        self.dna_database = np.array(list(problem.keys()))
        self.problem = problem
        a = self.dna_database.copy()
        b = self.dna_database.copy()
        c = self.dna_database.copy()
        np.random.shuffle(a)
        np.random.shuffle(b)
        np.random.shuffle(c)
        self.population = np.array([self.dna_database, a, b, c])

        self.population_size = population_size
        self.cross_rate = cross_rate
        self.mutation_rate = mutation_rate

    def get_fitness(self, population: np.ndarray):
        """
        取得目前世代的所有人的適應分數
        """

        return np.int16(MyTSP.calculate(population, self.problem))

    def cross_over(self, fitness: np.ndarray):
        """
        依適應分數做配種，留下好的種，把爛的種改掉
        """
        max_value = fitness.max()
        first_index = fitness.argmin()
        first_value = fitness[first_index]
        fitness[first_index] = max_value
        second_index = fitness.argmin()
        fitness[first_index] = first_value

        self.population[-1] = self.population[first_index]

        gape = 8
        # gape_amount = math.ceil(len(self.dna_database) / gape)
        dna_size = len(self.dna_database)

        """
        分成兩種交換，一種是把second的片段直接移到first的相同位置上；一種是把second的片段隨機移到first的隨機位置上
        """
        for i in range(int(self.population_size / 2)):
            rand_idx_first_0 = np.random.randint(0, dna_size - gape)
            rand_idx_first_1 = np.random.randint(0, dna_size - gape)

            if rand_idx_first_0 + gape > len(self.dna_database):
                rand_idx_first_0 = len(self.dna_database) - gape
            if rand_idx_first_1 + gape > len(self.dna_database):
                rand_idx_first_1 = len(self.dna_database) - gape

            temp_first = self.population[first_index].copy()
            temp_second = self.population[second_index].copy()

            temp_first[rand_idx_first_0:rand_idx_first_0 + gape] = temp_second[rand_idx_first_0:rand_idx_first_0 + gape]
            temp_first[rand_idx_first_1:rand_idx_first_1 + gape] = temp_second[rand_idx_first_1:rand_idx_first_1 + gape]

            self.population[i] = temp_first
            print(self.population[i], i)

        print()
        for i in range(int(self.population_size / 2), self.population_size - 1):
            rand_idx_first_0 = np.random.randint(0, dna_size - gape)
            rand_idx_first_1 = np.random.randint(0, dna_size - gape)
            rand_idx_second_0 = np.random.randint(0, dna_size - gape)
            rand_idx_second_1 = np.random.randint(0, dna_size - gape)

            temp_first = self.population[first_index].copy()
            temp_second = self.population[second_index].copy()

            temp_first[rand_idx_first_0:rand_idx_first_0 + gape] = temp_second[
                                                                   rand_idx_second_0:rand_idx_second_0 + gape]
            temp_first[rand_idx_first_1:rand_idx_first_1 + gape] = temp_second[
                                                                   rand_idx_second_1:rand_idx_second_1 + gape]

            self.population[i] = temp_first
            print(self.population[i], i)

    def mutation(self, pop_idx):
        """
        變異
        """
        pass

    def evolve(self, generation_amount):
        """
        執行世代交換的地方
        """
        pass


a = MGA(4, 0.1, 0.03, MyTSP.get_problem())
fitness = a.get_fitness(a.population)
print(fitness)
a.cross_over(fitness)
fitness = a.get_fitness(a.population)
print(fitness)
