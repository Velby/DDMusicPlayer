import utils
import os

class Song():

    def __init__(self, filename, styles=None, lastplay=0, dict=None, skipstart = 0):
        if not filename.endswith('.ogg'):
            raise TypeError('wrong extension '+filename)
        self.filename = filename
        self.filepath = os.path.join(utils.musicpath,self.filename)
        self.prevsong = None
        if dict:
            self.source = dict["source"]
            self.styles = dict["styles"]
            if "lastplay" in dict:
                self.lastplay = dict["lastplay"]
            else:
                self.lastplay = 0
            if "skipstart" in dict:
                self.skipstart = dict["skipstart"]
            else:
                self.skipstart = 0
        else:
            self.source = self.filename.split('_')[0]
            if not styles:
                self.styles = []
            else:
                self.styles = styles
            self.lastplay = lastplay
            self.skipstart = skipstart


    def todict(self):
        return {"filename":self.filename,"lastplay":self.lastplay,"styles":self.styles,"source":self.source, "skipstart":self.skipstart}

