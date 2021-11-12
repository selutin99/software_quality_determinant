import os
from typing import NoReturn

import matplotlib.pyplot as plt
import numpy as np

from ..utils.constants import Constants


class GraphService:
    def save_plot(self, calculation_id: str, Y: np.ndarray, X: np.ndarray) -> NoReturn:
        """
        Save plot of solving systems of difference equations
        :param calculation_id: cookie value is equal to user session id
        :param Y: matrix of solutions of a system of differential equations
        :param X: time interval from 0 to 1
        """
        plot_path: str = Constants.PATH_SOLUTION_GRAPHS_IMAGE + calculation_id + '.png'

        plt.rcParams["figure.figsize"] = (15, 8)

        for i in range(0, 15):
            plt.plot(X, Y[:, i], label='L' + str(i + 1))

        plt.legend()
        plt.savefig(plot_path)
        plt.clf()

    def save_petal_plots(self, calculation_id: str, Y: np.ndarray) -> NoReturn:
        """
        Function for creating petal diagrams showing changes
        in the system of differential equations over time
        :param calculation_id: cookie value is equal to user session id
        :param Y: atrix of solutions of a system of differential equations
        """
        graph_counter: int = 1
        graph_title: float = 0

        for i in range(0, len(Y) - 1, 12):
            if not os.path.exists(Constants.PATH_PETAL_GRAPHS_IMAGE + calculation_id):
                os.makedirs(Constants.PATH_PETAL_GRAPHS_IMAGE + calculation_id)
            plot_path: str = Constants.PATH_PETAL_GRAPHS_IMAGE + calculation_id + '/' + str(graph_counter) + '.png'
            self.__draw_petal_graph(
                graph_title=graph_title,
                stats=Y[i, :],
                minimals=np.append(Y[0, :] / 3, Y[0, 0] / 3)
            )
            plt.savefig(plot_path)

            graph_counter += 1
            graph_title += 0.25
        plt.clf()

    def __draw_petal_graph(self, graph_title: float, stats: list, minimals: list) -> NoReturn:
        variables_list = ['L' + str(i) for i in range(1, 16)]
        labels = np.array(variables_list)

        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False)
        stats = np.concatenate((stats, [stats[0]]))
        angles = np.concatenate((angles, [angles[0]]))
        labels = np.concatenate((labels, [labels[0]]))

        # Plot stuff
        fig = plt.figure()
        ax = fig.add_subplot(111, polar=True)

        ax.plot(angles, stats, 'o-', linewidth=2)
        ax.fill(angles, stats, alpha=0.25)

        ax.plot(angles, minimals, 'r', linewidth=2)
        ax.fill(angles, minimals, 'r', alpha=0.1)

        # Add legend and title for the plot
        plt.legend(labels=('Актуальные значения', 'Минимальные значения'), loc=1)

        ax.set_thetagrids(angles * 180 / np.pi, labels)
        ax.set_title("t=" + str(graph_title))
        ax.grid(True)
