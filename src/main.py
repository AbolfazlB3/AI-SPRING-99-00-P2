from AgentManager import AgentManager
from os import walk
import os


AM = AgentManager(10, 12)

print(AM.agents)

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
