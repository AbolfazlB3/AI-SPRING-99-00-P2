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

print(filenames)
print(levels)


game = Game(levels)

while game.load_next_level():

    AM = AgentManager(800, game)
    level = game.get_current_level()
    agent, inds, mins, maxs, avs = AM.converge(0.2, 300)
    score = game.get_score(agent)

    score = (score[0], round(score[1], 4))

    print(level[1])
    print(agent)
    print("Max possible score:\t", game.get_max_score(level[1]))
    print("Actual score:\t\t", score[1])
    print("Win: ", score[0])
    print(score)
    print("")

    GUI(agent, level[1], score, level[0])

    plt.plot(inds, mins, 'r')
    plt.plot(inds, maxs, 'b')
    plt.plot(inds, avs, 'g')
    plt.show()

    """
    for agent in AM.agents:
        print(game.get_score(agent), agent)
    """
