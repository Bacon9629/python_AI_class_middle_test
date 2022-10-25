import tsplib95
import numpy as np
import random

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


def deal_with_greedy(problem: dict) -> np.ndarray:
    """
    使用貪婪演算法
    :param problem: {地點名稱: [x, y], ...}，即要解的題目
    :return: 路線，city名稱
    """
    have_not_go_queue = list(problem.keys())
    start = random.choice(have_not_go_queue)  # 隨機選一個城市當作起始
    have_not_go_queue.remove(start)  # 把剛剛選到的起始城市從queue刪除
    result_list = [start]

    next_city = start
    for i in range(len(problem) - 1):
        next_city = find_nearest(next_city, have_not_go_queue, problem)[0]
        result_list.append(next_city)
        have_not_go_queue.remove(next_city)

    result_list.append(start)

    return np.array(result_list)


problem = MyTSP.get_problem()
result = deal_with_greedy(problem)
MyTSP.cal_draw(result, problem)
