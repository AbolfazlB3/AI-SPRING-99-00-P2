
class Game:

    def __init__(self, levels):
        self.levels = levels
        self.current_level_index = -1
        self.current_level_len = 0

    def load_next_level(self):
        self.current_level_index += 1
        self.current_level_len = len(self.levels[self.current_level_index])

    def get_score(self, actions):
        current_level = self.levels[self.current_level_index]
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
