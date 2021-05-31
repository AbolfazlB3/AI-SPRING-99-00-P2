import pygame as pg

STEP = 16
display_h = 223
display_w = 320


class GUI:
    
    def __init__(self, action, level):
        self.level = level
        self.state = []
        self.state = self.play(level, action)
        if(len(self.level) % 20 != 0):
            while(len(self.level) % 20 != 0):
                self.level += "_"
                self.state.append(0)
        self.gd = pg.display.set_mode((display_w, display_h))
        self.clk = pg.time.Clock()
        self.Map = pg.image.load("MAP.png")
        self.Mario = pg.image.load("MarioM.png")
        self.gd.blit(self.Map, (0, 0))
        self.gd.blit(self.Mario, (0, 169))
        pg.display.update()
        self.clk.tick(1)
        x = 16
        yy = 169
        for i in range(len(action)):
            if (action[i] == "1"):
                self.Mario = pg.image.load("MarioJ.png")
                yy = 169 - 31
            if (action[i] == "2"):
                self.Mario = pg.image.load("MarioD.png")
                yy = 169 + 8
            if (action[i] == "0"):
                self.Mario = pg.image.load("MarioM.png")
                yy = 169
            if(i < 12):
                self.gd.blit(self.Map, (0, 0))
                self.gd.blit(self.Mario, (x, yy))
                self.logic(self.level, self.state, i)
                x = x + 16
            if(i >= 12):
                self.gd.blit(self.Map, (0, 0))
                self.gd.blit(self.Mario, (x, yy))
                self.logic(self.level[i - 12:], self.state[i - 12:], 12)
            pg.display.update()
            self.clk.tick(3)
        pg.quit() 
    
    def logic(self, l, state, z):
        for i in range(len(l)):
            if(l[i] == "G"):
                if(state[i] == 0 or i - 1 > z):
                    self.gd.blit(pg.image.load("G.png"), (16 * i, 184))
                if(state[i] == 2 and i - 1 <= z):
                    self.gd.blit(pg.image.load("GD.png"), (16 * i, 190))
            if(l[i] == "L"):
                self.gd.blit(pg.image.load("L.png"), (16 * i, 160))
            if(l[i] == "M"):
                if(state[i] != 1 or i - 1 > z):
                    self.gd.blit(pg.image.load("M.png"), (16 * i, 184))
    
    def play(self, level, action):
        state = [0] * len(level)
        for i in range(1, len(level)):
            if(action[i - 1] != "1" and level[i] == "M"):
                state[i] = 1
            if(i > 1):
                if(action[i - 2] == "1" and level[i] == "G"):
                    state[i] = 2
        return state