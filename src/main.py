from os import walk
import os
import matplotlib.pyplot as plt

from gui import GUI
from Game import Game
from AgentManager import AgentManager


PATH = "../levels/"
_, _, filenames = next(walk(PATH))

levels = [
    (
        os.path.basename(level.name).split(".")[0],
        level.read().strip(),
        level.close()
    )[0:2] for level in [open(PATH+name) for name in filenames]
]

"""
print(filenames)
print(levels)
"""

game = Game(levels)

while game.load_next_level():

    AM = AgentManager(200, game)
    level = game.get_current_level()

    print(level[0])

    agent, inds, mins, maxs, avs, mxhs = AM.converge(0.2, 600)

    score = agent[1]

    print(level[1])
    print(agent[0])
    print("Max possible score:\t", game.get_max_score(level[1]))
    print("Actual score:\t\t", score[1])
    print("Win: ", score[0])
    print(score)
    print("")

    GUI(agent[0], level[1], score, level[0])

    fig = plt.gcf()
    fig.canvas.manager.set_window_title(level[0])
    plt.plot(inds, maxs, 'b')
    plt.plot(inds, mxhs, 'orange')
    plt.plot(inds, avs, 'g')
    plt.plot(inds, mins, 'r')
    plt.legend(["Best", "Avg of best 1/3", "Average",
                "Worst"], loc="lower right")
    plt.show()
