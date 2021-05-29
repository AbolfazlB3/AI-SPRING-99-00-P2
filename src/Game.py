
class Game:

    def __init__(self, levels):
        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0
        self.rewards = []

    def load_next_level(self):
        if(self.current_level_index + 1 == len(self.levels)):
            return False
        self.current_level_index += 1
        self.current_level_len = len(self.get_current_level()[1])
        return True

    def get_current_level(self):
        try:
            return self.levels[self.current_level_index]
        except:
            return None

    WIN_REWARD = 4.0
    FLAG_REWARD = 1.0
    MUSHROOM_REWARD = 2.0
    KILL_REWARD = 2.0
    JUMP_REWARD = -0.4
    MAX_STEP_REWARD = 0.2
    DEATH_REWARD = -2.5

    def get_score(self, actions):
        cll = self.current_level_len
        self.rewards = [None for i in range(cll)]
        current_name, current_level = self.get_current_level()
        if(current_level == None):
            return None
        res = self.get_score_rec(actions, current_level)

        reward = res[3]
        reward += res[1] * self.MAX_STEP_REWARD
        reward += res[2] * self.DEATH_REWARD

        return (res[2] == 0, reward)

    # (number of steps without dieing, max number of steps without dieing,
    #  number of deaths, total reward)
    def get_score_rec(self, actions, level, ind=0, air=False):

        if (self.rewards[ind] != None):
            return self.rewards[ind]

        cll = self.current_level_len
        act = actions[ind]
        cell = level[ind+1]

        if(ind == cll-1):
            self.rewards[ind] = (
                1, 1, 0, self.FLAG_REWARD if act == "1" else 0)
            return self.rewards[ind]

        reward = 0.0
        lose = False

        if ((cell == "G" and act != "1" and not air) or
                (cell == "L" and act != "2")):
            lose = True

        if (cell == "G" and air):
            reward += self.KILL_REWARD

        if (cell == "M" and act != "1"):
            reward += self.MUSHROOM_REWARD

        if(act == "1"):
            reward += self.JUMP_REWARD

        cont = self.get_score_rec(actions, level, ind+1, act == "1")

        steps = 0 if lose else cont[0] + 1

        self.rewards[ind] = (
            steps,
            max(steps, cont[1]),
            cont[2] + (1 if lose else 0),
            cont[3] + reward,
        )

        return self.rewards[ind]
