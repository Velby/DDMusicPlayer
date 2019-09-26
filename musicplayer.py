import utils
import writer
import songlist
import time




class MusicPlayer():

    def __init__(self):
        self.audio = utils.music
        self.ispaused = True
        self.cursong = None
        self.curstyle = None
        self.prevsong = None
        self.sorting = False
        self._deltat = 0
        self.cursongtime = 0
        self.songlist = songlist.SongList()
        self.styles = list(self.songlist.styles.values())
        self.writer = writer.Writer(self.helpstrings)
        self.writer_update()

    @property
    def helpstrings(self):
        return sorted([s.helpstring for s in self.styles])


    @property
    def keys(self):
        return {s.key:s for s in self.styles}

    def writer_update(self):
        topright = self.gettime()
        small = None
        if self.cursong:
            topleft = ", ".join(sorted(self.cursong.styles))
            caption = self.cursong.filename
        else:
            topleft = "Choose something to play"
            caption = "DD Music player"
        if self.curstyle and not self.ispaused:
            big = self.curstyle.name
            small = str(len(self.curstyle.songs)) + " songs"
        elif self.sorting:
            big = "SORTING"
            small = str(len(self.songlist.tosort)) + " songs"
        else:
            big = "PAUSED"
        self.writer.write(topleft=topleft, big=big, small=small, caption= caption, topright=topright)

    def tog_pause(self):
        if self.ispaused:
            self.audio.unpause()
            self.ispaused = False
        else:
            self.audio.pause()
            self.ispaused = True
        self.writer_update()

    def playStyle(self, letter):
        self.sorting = False
        try:
            style = self.keys[letter]
        except KeyError:
            print("no such style")
            return
        self.curstyle = style
        self.writer.write(big=style.name)
        self._playsong(style.nextsong())
        self.writer_update()

    def _playsong(self,s, goingback = False):
        self._deltat = 0
        if not goingback:
            s.prevsong = self.cursong
        self.ispaused = False
        self.cursong = s
        utils.music.load(s.filepath)
        utils.music.play(start=s.skipstart)
        self.cursongtime = utils.mixer.Sound(s.filepath).get_length()
        s.lastplay = time.time()
        self.songlist.persist()

    def playnext(self, hitnext=False):
        if not self.curstyle:
            if self.sorting and self.songlist.tosort:
                if not self.cursong or self.cursong.styles or hitnext:
                    self._playsong(min(self.songlist.tosort, key=lambda x: x.lastplay))
                else:
                    self._playsong(self.cursong)
            else:
                print("No style to play")
                return
        else:
            self._playsong(self.curstyle.nextsong())
        self.writer_update()

    def play_previous(self):
        if self.cursong.prevsong:
            self._playsong(self.cursong.prevsong, goingback = True)
            self.writer_update()

    def changesongstyle(self,letter):
        if not letter in self.keys:
            print("No such style")
            return
        st = self.keys[letter]
        so = self.cursong
        stylename = st.name
        if stylename in so.styles:
            so.styles.remove(stylename)
            if so.filename in st.songs:
                del(st.songs[so.filename])
                if not st.songs:
                    self.styles.remove(st)
        else:
            so.styles.append(stylename)
            if so in self.songlist.tosort:
                self.songlist.tosort.remove(so)
            st.addsong(so)
        self.songlist.persist()
        self.writer_update()

    def sortmode(self):
        if not self.sorting and not self.songlist.tosort:
            print("Nothing to sort")
            return
        if not self.sorting:
            self.curstyle = None
            self.sorting = True
        else:
            self.sorting = False
            self.curstyle = self.styles[0]
        self.playnext()

    def deletesong(self):
        s = self.cursong
        self.playnext(hitnext=True)
        self.songlist.deletesong(s)

    def gettime(self):
        if not self.cursong:
            lt = 0
            rt = 0
        else:
            lt = self.get_pos()/1000
            rt = self.cursongtime
        ls = time.strftime("%M:%S", time.gmtime(lt))
        rs = time.strftime("%M:%S", time.gmtime(rt))
        return ls+" / "+rs

    def scrub(self,sec):
        if self.cursong:
            newpos = self.get_pos() + sec*1000
            newpos = max(newpos, 0)
            if newpos > self.cursongtime*1000:
                self.playnext()
            else:
                self._deltat = newpos
                utils.music.play(0, newpos/1000)

    def get_pos(self):
        return utils.music.get_pos() + self._deltat

    def reset_all_playtimes(self):
        for s in self.songlist.allsongs.values():
            s.lastplay =0
        self.songlist.persist()
        print("all lastplay times set to 0")

