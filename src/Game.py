
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
        self.rewards = [None for i in range(self.current_level_len)]
        return True

    def get_current_level(self):
        try:
            return self.levels[self.current_level_index]
        except:
            return None

    def get_score(self, actions):
        current_name, current_level = self.get_current_level()
        if(current_level == None):
            return 0
        steps = 0
        for i in range(self.current_level_len - 1):
            current_step = current_level[i]
            if (current_step == '_'):
                steps += 1
            elif (current_step == 'G' and actions[i - 1] == '1'):
                steps += 1
            elif (current_step == 'L' and actions[i - 1] == '2'):
                steps += 1
            else:
                break
        return steps == self.current_level_len - 1, steps

    WIN_REWARD = 4.0
    FLAG_REWARD = 1.0
    MUSHROOM_REWARD = 2.0
    KILL_REWARD = 2.0
    JUMP_REWARD = -0.4

    # (number of steps without dieing, max number of steps without dieing,
    #  number of deaths, total reward)
    def get_score_rec(self, actions, level, ind, air=False):

        if (self.rewards[ind] != None):
            return self.rewards[ind]

        cll = self.current_level_len
        action = actions[ind]

        if(ind == cll-1):
            self.rewards[ind] = (
                1, 1, 0, self.FLAG_REWARD if action == "1" else 0
            )
            return self.rewards[ind]

        reward = 0.0
        lose = False

        if():
            pass

        for i in range(self.current_level_len - 1):
            current_step = current_level[i]
            if (current_step == '_'):
                steps += 1
            elif (current_step == 'G' and actions[i - 1] == '1'):
                steps += 1
            elif (current_step == 'L' and actions[i - 1] == '2'):
                steps += 1
            else:
                break
        return steps == self.current_level_len - 1, steps
