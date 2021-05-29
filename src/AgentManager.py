import random
import numpy as np


class AgentManager:

    def __init__(self, agent_num, level_len, game):
        self.game = game
        self.agent_num = agent_num
        self.level_len = level_len
        self.current_generation = 0
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
        
        chance, _ = self.prob()
        next_g = np.random.choice(self.agents, len(self.agents) // 2, p=chance)
        parents = np.random.choice(self.agents, (len(self.agents) - (len(self.agents) // 2)) * 2, p=chance)
        for i in range(len(parents), 2):
            next_g.append(self.recombination(parents[i], parents[i + 1]))
        for i in reange(next_g):
            next_g[i] = self.mutation(next_g[i])
        self.agents = next_g
        self.current_generation += 1
    
    def prob(self):
        chance = [0] * len(self.agents)
        Sum = 0
        p = 100000
        for i in range(len(self.agents)):
            j = game.get_score(self.agents[i])
            if(j < p):
                p = j
            chance[i] = j
            Sum += j
        if(p < 0):
            chance[:] = [(x - p) / Sum for x in chance]
        else:
            chance[:] = [x / Sum for x in chance]
        return (chance, Sum)

    def converge(self, limit, iteration_limit):
        s = 1000
        while(s > limit and self.current_generation < iteration_limit):
            _, s1 = self.prob()
            self.go_next_generation()
            _, s2 = self.prob()
            s = abs(s2 - s1)

a = AgentManager(2, 10)
print(a.agents)