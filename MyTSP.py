import tsplib95
from matplotlib import pyplot as plt
import numpy as np


class MyTSP:

    @staticmethod
    def get_problem() -> dict:
        return tsplib95.load('./berlin52.tsp').node_coords

    @staticmethod
    def cal_draw(point_queue: np.ndarray, problem_dict: dict) -> None:
        """
        印出計算值並且畫出來
        :param point_queue: 前往各城市點的順序
        :param problem_dict: 題目，從tsplib95.load('./berlin52.tsp').node_coords來的
        :return: None
        """
        if len(point_queue.shape) != 1:
            raise TypeError("len(point_queue.shape) should be '1'")

        list_x = []
        list_y = []
        for i in point_queue:
            list_x.append(problem_dict[i][0])
            list_y.append(problem_dict[i][1])
        plt.plot(list_x, list_y)
        plt.scatter(list_x, list_y, color='blue')

        plt.scatter(problem_dict[point_queue[0]][0], problem_dict[point_queue[0]][1], color='red')
        plt.scatter(problem_dict[point_queue[-2]][0], problem_dict[point_queue[-2]][1], color='green')

        plt.show()
        print("total distance: ", MyTSP.calculate(point_queue, problem_dict))

    @staticmethod
    def calculate(point_queue: np.ndarray, problem_dict: dict) -> np.ndarray:
        """
        計算並回傳總距離
        :param point_queue: 前往各城市點的順序
        :param problem_dict: 題目，從tsplib95.load('./berlin52.tsp').node_coords來的
        :return: 此次行程的總距離
        """
        if len(point_queue.shape) == 1:
            result = np.zeros(1)
            for i in range(point_queue.shape[0] - 1):
                a = point_queue[i]
                b = point_queue[i + 1]
                result[0] += np.sqrt(
                    (problem_dict[a][0] - problem_dict[b][0]) ** 2 + (problem_dict[a][1] - problem_dict[b][1]) ** 2
                )
            return result
        else:
            result = np.zeros(point_queue.shape[0])
            for j in range(point_queue.shape[0]):
                for i in range(point_queue.shape[1] - 1):
                    a = point_queue[j][i]
                    b = point_queue[j][i + 1]
                    result[j] += np.sqrt(
                        (problem_dict[a][0] - problem_dict[b][0]) ** 2 + (problem_dict[a][1] - problem_dict[b][1]) ** 2
                    )
            return result
