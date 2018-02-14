import utils
import pygame
import musicplayer


styles= {"f":"fight", "n":"nature"}
helpstr = ", ".join(["[{0}]: {1}".format(k,v) for (k,v) in styles.items()])

SONG_END = pygame.USEREVENT + 1
player = musicplayer.MusicPlayer()

CLOCKTICK, t = pygame.USEREVENT+2, 250
pygame.time.set_timer(CLOCKTICK, t)


def game_loop():
    while True:
        for event in pygame.event.get():
            shift = pygame.key.get_mods() & pygame.KMOD_SHIFT
            if event.type == CLOCKTICK:
                player.writer_update()
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if 96 < event.key <= 122:
                    letter = chr(event.key)
                    if shift or player.sorting:
                        player.changesongstyle(letter)
                    else:
                        player.playStyle(letter)
                if event.key == pygame.K_SPACE:
                    player.tog_pause()
                if event.key == pygame.K_RIGHT:
                    if shift:
                        player.scrub(10)
                    else:
                        player.playnext(hitnext=True)
                if event.key == pygame.K_LEFT:
                    if shift:
                        player.scrub(-10)
                    else:
                        player.play_previous()
                if event.key == pygame.K_1 and shift:
                    player.sortmode()
                if event.key==pygame.K_DELETE and shift:
                    player.deletesong()
                if event.key == pygame.K_KP0 and shift:
                    player.reset_all_playtimes()
            if event.type == utils.SONG_END:
                player.playnext()


game_loop()
pygame.quit()
quit()
