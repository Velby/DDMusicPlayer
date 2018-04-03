import pygame
import os
import json



display_width = 480
display_height = 300
musicpath = os.path.expanduser('~/Music/player/music')
songdatafile = 'songlist.json'

pygame.init()
pygame.mixer.init()
music = pygame.mixer.music
mixer = pygame.mixer
screen = pygame.display.set_mode((display_width,display_height))
display = pygame.display
music.get_pos()

SONG_END = pygame.USEREVENT + 1

music.set_endevent(SONG_END)


def loadjsonfile(filename):
    return json.loads(open(filename,'r').read())

def dumpjsonfile(filename, jsono):
    open(filename,'w').write(json.dumps(jsono, indent=4))
