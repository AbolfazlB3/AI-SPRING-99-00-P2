import random
import numpy as np


class AgentManager:

    def __init__(self, agent_num, level_len):
        self.agent_num = agent_num
        self.level_len = level_len
        self.agents = []

        for i in range(agent_num):
            self.agents.append(self.create_new_agent(level_len))

    init_prob = {
        "move": 0.45,
        "jump": 0.30,
        "dash": 0.25,
    }

    def create_new_agent(self, l):
        pr = self.init_prob
        pmove = pr["move"]
        pjump = pr["jump"]
        pdash = pr["dash"]
        res = ""
        for i in range(l):
            rnd = random.random() * (pmove + pjump + pdash)
            if(rnd < pmove):
                res += "0"
            elif (rnd < pmove + pjump):
                res += "1"
            elif (rnd <= pmove + pjump + pdash):
                res += "2"
        res = self.fix_agent(res)
        return res
    
    def fix_agent(self, agent):
        list_agent = list(agent)
        for i in range(1, len(list_agent)):
            if(list_agent[i - 1] == "1"):
                list_agent[i - j] = "0"
        return ''.join(list_agent)
    
    def recombination(self, agent1, agent2):
        index = random.randint(0, len(agent1))
        return self.fix_agent(agent1[:index] + agent2[index:])
    
    def go_next_generation(self):
        chance = [0] * len(self.agents)
        Sum = 0
        for i in range(len(self.agents)):
            j = i
            chance[i] = j
            Sum += j
        chance[:] = [x / Sum for x in chance]
        next_g = np.random.choice(self.agents, len(self.agents) // 2, chance)

a = AgentManager(2, 10)
print(a.agents)