from os import walk
import os
import matplotlib.pyplot as plt

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

    AM = AgentManager(600, game)
    level = game.get_current_level()
    agent, inds, mins, maxs, avs = AM.converge(0.5, 1500)
    score = game.get_score(agent)

    print(level[1])
    print(agent)
    print(score)
    print("")

    plt.plot(inds, mins, 'r')
    plt.plot(inds, maxs, 'b')
    plt.plot(inds, avs, 'g')
    plt.show()

    """
    for agent in AM.agents:
        print(game.get_score(agent), agent)
    """
