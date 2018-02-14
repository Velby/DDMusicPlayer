import utils
import os

class Song():

    def __init__(self, filename, styles=None, lastplay=0, dict=None):
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
        else:
            self.source = self.filename.split('_')[0]
            if not styles:
                self.styles = []
            else:
                self.styles = styles
            self.lastplay = lastplay


    def todict(self):
        return {"filename":self.filename,"lastplay":self.lastplay,"styles":self.styles,"source":self.source}

