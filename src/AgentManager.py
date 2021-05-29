import random
import numpy as np
from Game import Game
import math


class AgentManager:

    def __init__(self, agent_num, game):
        agent_num += 4-(agent_num % 4)
        self.game = game
        self.agent_num = agent_num
        self.level_len = game.current_level_len
        self.current_generation = 0
        self.agents = []
        self.maxs = []
        self.mins = []
        self.avs = []

        for i in range(agent_num):
            self.agents.append(self.create_new_agent(self.level_len))

    init_prob = {
        "move": 0.38,
        "jump": 0.38,
        "dash": 0.24,
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
        for i in range(len(list_agent) - 1):
            if(list_agent[i] == "1" and list_agent[i+1] != "0"):
                list_agent[i + random.randint(0, 1)] = "0"
        return ''.join(list_agent)

    MUTATION_CHANCE = 0.2
    BIASED_MUTATION_CHANCE = 0.75

    def mutate(self, agent):
        if(random.random() > self.MUTATION_CHANCE):
            return agent

        indices = np.random.choice(
            len(agent), int(np.log2(len(agent))), replace=False)

        list_agent = list(agent)

        for i in indices:
            if(list_agent[i] == "1"):
                if(random.random() > self.BIASED_MUTATION_CHANCE):
                    list_agent[i] = "0"
                else:
                    list_agent[i] = str(random.randint(1, 2))
            else:
                list_agent[i] = str(random.randint(0, 2))

        return ''.join(list_agent)

    def recombination(self, agent1, agent2):
        index = random.randint(0, len(agent1))
        return (agent1[:index] + agent2[index:], agent2[:index] + agent1[index:])

    def go_next_generation(self, chance):

        next_g_inds = np.random.choice(
            len(self.agents), len(self.agents) // 2, p=chance)
        next_g = [self.agents[x] for x in next_g_inds]
        parent_inds = np.random.choice(
            len(self.agents), len(self.agents) // 2, p=chance)
        parents = [self.agents[x] for x in parent_inds]

        for i in range(0, len(parents), 2):
            recomb = self.recombination(parents[i], parents[i + 1])
            next_g.append(recomb[0])
            next_g.append(recomb[1])

        for i in range(len(next_g)):
            next_g[i] = self.fix_agent(self.mutate(next_g[i]))

        self.agents = next_g
        self.current_generation += 1

    RESCALE_CONSTANT = 0.7

    def rescale(self, x):
        r = x / (
            (max(self.game.MUSHROOM_REWARD, self.game.KILL_REWARD/2.0) + self.game.MAX_STEP_REWARD) *
            self.RESCALE_CONSTANT * self.game.current_level_len +
            self.game.WIN_REWARD
        )
        return 0.5*(r/(1+abs(r))+1)

    def rescale2(self, x):
        b = 0.5 * self.game.current_level_len
        xb = x/b
        return x+b if x > 0 else b*(abs(xb)+1)*math.exp(xb)

    def rescale3(self, x):
        b = 1.5 * self.game.current_level_len
        return math.exp(x/b)

    def prob(self):
        chance = [0] * len(self.agents)
        Sum = 0
        scoreSum = 0
        mns = 1000000
        mxs = -1000000
        for i in range(len(self.agents)):
            j = self.game.get_score(self.agents[i])[1]
            scoreSum += j
            mxs = max(mxs, j)
            mns = min(mns, j)
            j = self.rescale3(j)
            chance[i] = j
            Sum += j
        chance = [x / Sum for x in chance]
        return (chance, scoreSum/len(self.agents), mns, mxs)

    MIN_CONVERGE_NUM = 20

    def converge(self, limit, iteration_limit):
        s = 1000
        slast = -10**6
        dss = [limit + 1]
        firstSuccess = False
        inds = []

        best_agent = None
        best_result = (False, -1000000)

        while(self.current_generation < iteration_limit):
            probs, s, mns, mxs = self.prob()
            gen_best_agent = self.agents[probs.index(max(probs))]
            gen_best_agent_score = self.game.get_score(gen_best_agent)

            if((not firstSuccess) and gen_best_agent_score[0]):
                firstSuccess = True
                print("first success", self.current_generation,
                      gen_best_agent_score)

            if(gen_best_agent_score[1] > best_result[1]):
                best_result = gen_best_agent_score
                best_agent = gen_best_agent

            inds.append(self.current_generation)
            self.mins.append(mns)
            self.maxs.append(mxs)
            self.avs.append(s)

            ds = abs(s - slast)

            finish = True
            for dsi in dss[-self.MIN_CONVERGE_NUM:]:
                if(dsi > limit):
                    finish = False

            if finish:
                break

            dss.append(ds)
            slast = s
            self.go_next_generation(probs)

        print("regen num", self.current_generation)

        return best_agent, inds, self.mins, self.maxs, self.avs
