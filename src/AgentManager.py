import random


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
            elif (rnd < pmove + pjump + pdash):
                res += "2"
        return res
