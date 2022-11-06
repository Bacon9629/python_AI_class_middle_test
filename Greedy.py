import tsplib95
import numpy as np
import random
from matplotlib import pyplot as plt

from MyTSP import MyTSP


def find_nearest(start_city_name, queue: list, problem: dict) -> list:
    """
    尋找離現在這個點最近的其他點
    :param start_city_name: 從這個點開始，輸入這個點的名稱
    :param queue: 要尋找最近點的候選名單，會從這些名單內挑選最近點
    :param problem: {地點名稱: [x, y], ...}，即要解的題目
    :return: [cityname: int, distance: float]，離 start_city_name 最近的點與距離
    """
    _min = [0, 1000000000]  # [index, distance]
    for index in queue:
        if index == start_city_name:
            continue
        _dis = MyTSP.calculate(np.array([start_city_name, index]), problem)
        if _dis < _min[1]:
            _min = [index, _dis]
    return _min


def find_nearest_with_epsilon(start_city_name, queue: list, problem: dict, probability: float) -> list:
    """
    尋找離現在這個點最近的其他點
    :param start_city_name: 從這個點開始，輸入這個點的名稱
    :param queue: 要尋找最近點的候選名單，會從這些名單內挑選最近點
    :param problem: {地點名稱: [x, y], ...}，即要解的題目
    :param probability: [0, 1]隨機探索機率，機率越大則選擇隨機路線的機率越高
    :return: [cityname: int, distance: float]，離 start_city_name 最近的點與距離
    """

    if random.random() < probability:
        rand_index = random.choice(queue)
        _dis = MyTSP.calculate(np.array([start_city_name, rand_index]), problem)
        return [rand_index, _dis]


    _min = [0, 1000000000]  # [index, distance]
    for index in queue:
        if index == start_city_name:
            continue
        _dis = MyTSP.calculate(np.array([start_city_name, index]), problem)
        if _dis < _min[1]:
            _min = [index, _dis]
    return _min


def deal_once(problem: dict, p: float) -> np.ndarray:
    """
    使用貪婪演算法
    :param problem: {地點名稱: [x, y], ...}，即要解的題目
    :param p: 隨機的機率
    :return: 路線，city名稱
    """
    have_not_go_queue = list(problem.keys())
    start = random.choice(have_not_go_queue)  # 隨機選一個城市當作起始
    have_not_go_queue.remove(start)  # 把剛剛選到的起始城市從queue刪除
    result_list = [start]

    next_city = start
    for i in range(len(problem) - 1):
        next_city = find_nearest_with_epsilon(next_city, have_not_go_queue, problem, p)[0]
        result_list.append(next_city)
        have_not_go_queue.remove(next_city)

    result_list.append(start)
    result = np.array(result_list)
    return result, MyTSP.calculate(result, problem)


def deal_with_greedy_epsilon(problem: dict, iteration: int) -> [np.ndarray, list]:
    """
    使用貪婪演算法搭配一點隨機性
    :param problem: {地點名稱: [x, y], ...}，即要解的題目
    :param iteration: 迭代次數
    :return: [最好的路線, 此次蝶待的最佳距離]
    """

    best_, best_dis = deal_once(problem, 0)
    history = [best_dis]
    history_iteration = [0]

    for i in range(iteration):
        temp, temp_dis = deal_once(problem, 0.1)
        if temp_dis < best_dis:
            best_, best_dis = temp, temp_dis
            history.append(best_dis)
            history_iteration.append(i)
        if i % 1000 == 0:
            print("iteration: ", i)

    return best_, history, history_iteration



iteration = 100000

problem = MyTSP.get_problem()
result, history, history_iteration = deal_with_greedy_epsilon(problem, iteration)
# plt.subplot(121)
plt.figure('a')
# plt.plot([i for i in range(len(history))], history)
plt.plot(history_iteration, history)
plt.show()
# plt.subplot(122)
plt.figure('b')
MyTSP.cal_draw(result, problem)
print(result)
print(0.1)

