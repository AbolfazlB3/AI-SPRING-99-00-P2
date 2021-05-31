import pygame as pg

STEP = 16
display_h = 223
display_w = 320

# images address
IMA = "../res/images/"
FNA = "../res/fonts/"


class GUI:

    def __init__(self, action, level, point=None, name="Mario"):
        self.level = level + "F"
        self.action = action
        self.point = point

        pg.init()
        self.assets = {
            "map": pg.image.load(IMA + "MAP.png"),
            "mario_m": pg.image.load(IMA + "MarioM.png"),
            "mario_d": pg.image.load(IMA + "MarioD.png"),
            "mario_j": pg.image.load(IMA + "MarioJ.png"),
            "g": pg.image.load(IMA + "G.png"),
            "gd": pg.image.load(IMA + "GD.png"),
            "l": pg.image.load(IMA + "L.png"),
            "m": pg.image.load(IMA + "M.png"),
            "flag": pg.image.load(IMA + "flag.png"),
            "font": pg.font.Font(FNA + "Arial.ttf", 12),
        }

        self.state = []
        self.state = self.play(level, action)
        if(len(self.level) % 20 != 0):
            while(len(self.level) % 20 != 0):
                self.level += "_"
                self.state.append(0)
        self.gd = pg.display.set_mode((display_w, display_h))
        pg.display.set_caption(name)
        self.clk = pg.time.Clock()

        self.Map = self.assets["map"]
        self.Mario = self.assets["mario_m"]

        self.run()

    def go_next(self):
        if(self.frame < len(self.action)-1):
            self.frame += 1
        if(self.frame == len(self.action)-1):
            self.paused = True

    def go_prev(self):
        if(self.frame > -1):
            self.frame -= 1

    def run(self):

        self.paused = True
        self.running = True
        self.frame = -1

        delay = 0.0

        while(self.running):

            for event in pg.event.get():
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_a:
                        self.go_prev()
                        self.paused = True
                        break
                    if event.key == pg.K_d:
                        self.go_next()
                        self.paused = True
                        break
                    if event.key == pg.K_SPACE:
                        self.paused = not self.paused
                        break
                    if event.key == pg.K_ESCAPE or event.key == pg.K_RETURN:
                        self.running = False
                        break
                if event.type == pg.QUIT:
                    self.running = False
                    break

            self.draw(self.frame)
            delay += self.clk.tick(60)

            ANIM_DELAY = 500

            if(delay >= ANIM_DELAY):
                delay -= ANIM_DELAY
                if(not self.paused):
                    self.go_next()

        pg.quit()

    def draw(self, i):
        act = "0"
        x = 16 * min(i+1, 13)
        yy = 169

        if (i < 0):
            x = 0
        else:
            act = self.action[i]

        if (act == "1"):
            self.Mario = self.assets["mario_j"]
            yy = 169 - 31
        if (act == "2"):
            self.Mario = self.assets["mario_d"]
            yy = 169 + 8
        if (act == "0"):
            self.Mario = self.assets["mario_m"]
            yy = 169

        self.gd.blit(self.Map, (0, 0))

        if(i < 12):
            self.logic(self.level, self.state, i)
        else:
            self.gd.blit(self.Map, (0, 0))
            self.logic(self.level[i - 12:], self.state[i - 12:], 12)

        self.gd.blit(self.Mario, (x, yy))

        text_color = (30, 38, 50)

        text = self.assets["font"].render(
            "Paused" if self.paused else "Playing", True, text_color)
        self.gd.blit(text, (5, 5))

        if(self.point != None):
            self.gd.blit(
                self.assets["font"].render(str(self.point), True, text_color),
                (5, 20)
            )

        pg.display.update()

    def logic(self, l, state, z):
        for i in range(len(l)):
            if(l[i] == "G"):
                if(state[i] == 0 or i - 1 > z):
                    self.gd.blit(self.assets["g"], (16 * i, 184))
                if(state[i] == 2 and i - 1 <= z):
                    self.gd.blit(self.assets["gd"], (16 * i, 190))
            if(l[i] == "L"):
                self.gd.blit(self.assets["l"], (16 * i, 160))
            if(l[i] == "M"):
                if(state[i] != 1 or i - 1 > z):
                    self.gd.blit(self.assets["m"], (16 * i, 184))
            if(l[i] == "F"):
                self.gd.blit(self.assets["flag"], (16 * i, 150))

    def play(self, level, action):
        state = [0] * len(level)
        for i in range(1, len(level)):
            if(action[i - 1] != "1" and level[i] == "M"):
                state[i] = 1
            if(i > 1):
                if(action[i - 2] == "1" and level[i] == "G"):
                    state[i] = 2
        return state
