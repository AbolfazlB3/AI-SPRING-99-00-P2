from os import walk
import os

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

    AM = AgentManager(10, game.current_level_len)

    print(game.get_current_level())

    for agent in AM.agents:
        print(game.get_score(agent), agent)
