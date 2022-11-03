from MyTSP import MyTSP
import numpy as np
from matplotlib import pyplot as plt


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
        self.population = np.array([self.dna_database, a, b, c] + [c for i in range(population_size - 4)])

        self.population_size = population_size
        self.cross_rate = cross_rate
        self.mutation_rate = mutation_rate

        self.cross_over_count = 0

    def get_fitness(self, population: np.ndarray):
        """
        取得目前世代的所有人的適應分數
        """

        return np.int16(MyTSP.calculate(population, self.problem))

    def cross_over(self, fitness: np.ndarray):
        """
        依適應分數做配種，留下好的種，把爛的種改掉
        """
        self.cross_over_count += 1
        # 找出fitness最好的兩個值
        max_value = fitness.max()
        first_index = fitness.argmin()
        first_value = fitness[first_index]
        fitness[first_index] = max_value
        second_index = fitness.argmin()
        fitness[first_index] = first_value

        self.population[-1] = self.population[first_index]
        self.population[-2] = self.population[second_index]

        gape = 8
        # gape_amount = math.ceil(len(self.dna_database) / gape)
        dna_size = len(self.dna_database)

        """
        分成兩種交換，一種是把second的片段直接移到first的相同位置上；一種是把second的片段隨機移到first的隨機位置上
        """
        # for i in range(int(self.population_size)-1):
        for i in range(int(self.population_size / 2) - 1):
            rand_idx_first_0 = np.random.randint(0, dna_size - gape)
            rand_idx_first_1 = np.random.randint(0, dna_size - gape)

            temp_first = self.population[first_index].copy()
            temp_second = self.population[second_index].copy()

            temp_first[rand_idx_first_0:rand_idx_first_0 + gape] = temp_second[rand_idx_first_0:rand_idx_first_0 + gape]
            temp_first[rand_idx_first_1:rand_idx_first_1 + gape] = temp_second[rand_idx_first_1:rand_idx_first_1 + gape]

            temp_first = self.remove_repeat_value(temp_first)

            # print(temp_first, i)
            self.population[i] = temp_first
            # print(self.population[i])

        # print()
        for i in range(int(self.population_size / 2) - 1, self.population_size - 2):
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

            temp_first = self.remove_repeat_value(temp_first)

            self.population[i] = temp_first
            # print(self.population[i], i)

        # 若first和second一致，則把second mutation
        # 找出fitness最好的兩個值
        if np.array_equal(self.population[-1], self.population[-2]):
            self.mutation(-2)

        # print()

    def remove_repeat_value(self, _list: np.ndarray) -> np.ndarray:
        """
        解決重複元素問題
        :param _list: 目標list
        :return: 解決結果
        """
        # 排除重複元素 - start
        copy_database = np.copy(self.dna_database)
        database_status = np.ones(copy_database.shape[0], dtype='uint16')
        temp_first_status = np.zeros(_list.shape[0], dtype='bool')

        # 驗證是否有重複或沒使用到的元素
        for index, item in enumerate(self.dna_database):
            temp_index = np.isin(_list, [item])
            _sum = np.sum(temp_index)
            if _sum == 1:
                database_status[index] = 0
            elif _sum > 1:
                temp_first_status[temp_index] = True
                database_status[index] = 2

        # 將沒使用到的元素取代重複元素
        bad_status_index = database_status > 0
        a = self.dna_database[bad_status_index]
        np.random.shuffle(a)
        _list[temp_first_status] = a
        # 排除重複元素 - end

        return _list

    def mutation(self, pop_idx):
        """
        變異
        """
        size = self.dna_database.shape[0]
        for i in range(size):
            if np.random.randint(size) > 3:
                continue
            a = np.random.randint(size)
            b = np.random.randint(size)
            while a == b:
                a = np.random.randint(size)
                b = np.random.randint(size)
            # print(self.population.shape)
            # print(pop_idx, a, b)
            self.population[pop_idx, a], self.population[pop_idx, b] = self.population[pop_idx, b], self.population[pop_idx, a]

        pass

    def evolve(self, generation_amount):
        """
        執行世代交換的地方
        """
        history_y = []
        for i in range(generation_amount):
            fitness = self.get_fitness(self.population)
            history_y.append(np.min(fitness))
            self.cross_over(fitness)
            if i % 500 == 0:
                print(i, " - ", fitness)

        fitness = self.get_fitness(self.population)
        best_index = np.argmin(fitness)
        history_y.append(np.min(fitness))
        return fitness[best_index], self.population[best_index], history_y


a = MGA(60, 0.1, 0.03, MyTSP.get_problem())
score, policy, history_y = a.evolve(100000)

print(score, policy)

plt.figure('a')
# plt.subplot(211)
plt.plot(history_y)
plt.show()
# plt.subplot(212)
plt.figure('b')
MyTSP.cal_draw(policy, MyTSP.get_problem())
