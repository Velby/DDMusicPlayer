import random

class Style():

    def __init__(self, stylename):
        self.name = stylename
        self.key = self.name[0].lower()
        self.songs = {}

    def addsong(self, s):
        self.songs[s.filename] = s

    def nextsong(self):
        return min(self.songs.values(), key=lambda x: x.lastplay + random.random())

    @property
    def helpstring(self):
        return "{1}".format(self.key, self.name)

    def remove(self, song):
        if song.filename in self.songs:
            del(self.songs[song.filename])
