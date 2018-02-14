import os
import utils
from song import Song
import style

#TODO add more metadata like list of styles and lost files

class SongList():

    def __init__(self):
        self.listpath = os.path.join(utils.musicpath,utils.songdatafile)
        self.allsongs = {}
        self.tosort = []
        self.styles = {}
        self.lostfiles = {}
        self.load_from_file()
        self.persist()

    @property
    def jsondata(self):
        songs = {k:v.todict() for k, v in self.allsongs.items()}
        lostsongs = {k:v.todict() for k, v in self.lostfiles.items()}
        return {
            "styles": sorted(self.styles.keys()),
            "songs": songs,
            "lostfiles": lostsongs
        }

    def load_from_file(self):
        ls = os.listdir(utils.musicpath)
        if not os.path.isfile(self.listpath):
            utils.dumpjsonfile(self.listpath, self.jsondata)
        else:
            alldata = utils.loadjsonfile(self.listpath)
            if "songs" in alldata:
                self.allsongs =  {k:Song(k, dict=v) for k,v in alldata["songs"].items()}
            else:
                print("Didn't find any songs in songs.json")
            if "lostfiles" in alldata:
                prevlost = alldata["lostfiles"]
            else:
                prevlost = {}
        for fn in ls:
            if not fn.endswith('.ogg'):
                continue
            if fn not in self.allsongs:
                if fn in prevlost:
                    self.allsongs[fn] = Song(fn,dict=prevlost[fn])
                else:
                    self.allsongs[fn] = Song(fn)
                    print("added new song: "+fn)
            if fn in self.allsongs and fn in prevlost:
                del(prevlost[fn])
        self.lostfiles = {k:Song(k,dict=v) for k,v in prevlost.items()}

        for fn,s in list(self.allsongs.items()):
            if not os.path.isfile(s.filepath):
                print("lost file: "+fn)
                del(self.allsongs[fn])
                self.lostfiles[fn] = s
            else:
                for t in s.styles:
                    if t not in self.styles:
                        self.styles[t] = style.Style(t)
                    self.styles[t].addsong(s)
                if not s.styles:
                    self.tosort.append(s)

    def persist(self):
        utils.dumpjsonfile(self.listpath, self.jsondata)

    def deletesong(self,s):
        del(self.allsongs[s.filename])
        for t in s.styles:
            if t in self.styles and s in self.styles[t].songs.values():
                self.styles[t].remove(s)
        if s in self.tosort:
            self.tosort.remove(s)
        os.remove(s.filepath)



