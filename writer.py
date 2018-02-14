import utils
import pygame

font='freesansbold.ttf'
black = (0,0,0)
white = (255,255,255)

class Writer():

    def __init__(self, helptexts):
        self.helpstrings = helptexts
        self.screen = utils.screen
        self.display = utils.display
        self._caption = "Let's play"
        self._topleft = "please select an ambiance"
        self._topright = ""
        self._big = "PAUSE"
        self._small = ""
        self._bot = ", ".join(self.helpstrings[:9])
        self._bot2 = ", ".join(self.helpstrings[9:])
        self.unpausetext = ""
        self.write()

    @property
    def topleft(self):
        return self._topleft

    @topleft.setter
    def topleft(self, val):
        self._topleft = val
        self._single_write(val, pos=1)

    @property
    def topright(self):
        return self._topright

    @topright.setter
    def topright(self, val):
        self._topright = val
        self._single_write(val, pos=4)

    @property
    def bot(self):
        return self._bot

    @bot.setter
    def bot(self, val):
        self._bot = val
        self._single_write(val, pos=3)

    @property
    def bot2(self):
        return self._bot2

    @bot2.setter
    def bot2(self, val):
        self._bot2 = val
        self._single_write(val, pos=5)

    @property
    def big(self):
        return self._big

    @big.setter
    def big(self, val):
        self._big = val
        self._single_write(val, pos=2, size=80)

    @property
    def small(self):
        return self._small

    @small.setter
    def small(self, val):
        self._small = val
        self._single_write(val, pos=6)

    @property
    def caption(self):
        return self._caption

    @caption.setter
    def caption(self, val):
        self._caption = val
        self.display.set_caption(val)

    def text_objects(self, text, font):
        textSurface = font.render(text, True, black)
        return textSurface, textSurface.get_rect()

    def _single_write(self, t, size=15, font=font, pos=2):
        x, y = self.screen.get_size()
        text = pygame.font.Font(font, size)
        textSurf, textRec = self.text_objects(t, text)
        if pos == 2:
            textRec.center = ((x / 2), (y / 2))
        if pos == 1:
            textRec.topleft = (5, 5)
        if pos == 3: #bottom 1
            textRec.bottomleft = (5 , y- 5 - textRec.height)
        if pos == 4:
            textRec.topright = (x-5, 5)
        if pos == 5: #bottom 2
            textRec.bottomleft = (5 , y-5)
        if pos == 6:
            textRec.midtop = (x/2, y/2+60)
        self.screen.blit(textSurf, textRec)

    def write(self, small = None, big=None, bottom=None, topleft=None, topright=None, caption=None, bot2=None):
        self.screen.fill(white)
        if not type(big) is str:
            big = self.big
        self.big = big
        if not type(topright) is str:
            topright = self.topright
        self.topright = topright
        if not type(bottom) is str:
            bottom = self.bot
        self.bot = bottom
        if not type(topleft) is str:
            topleft = self.topleft
        self.topleft = topleft
        if not type(caption) is str:
            caption = self.caption
        self.caption = caption
        if not type(bot2) is str:
            bot2 = self.bot2
        self.bot2 = bot2
        if not type(small) is str:
            small = self.small
        self.small = small
        self.display.update()

    def pause(self):
        self.unpausetext = self.big
        self.write(big="PAUSE")

    def unpause(self):
        self.write(big=self.unpausetext)
