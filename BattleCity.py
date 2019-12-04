from game_mech import interface_classes as ic
from game_mech import conf
from game_mech import music
import pygame
import sys
import os
sys.path.insert(0, os.path.join("game_mech"))


pygame.init()

win = pygame.display.set_mode((conf.win_width, conf.win_height))
clock = pygame.time.Clock()


def game():
    while game_stage[0] != conf.END:
        clock.tick(conf.FPS)
        music.music_class.update_music(game_stage[0])
        if game_stage[0] == conf.MENU:
            ic.menu_class.menu_cycle(game_stage, win)
        if game_stage[0] == conf.GAME:
            ic.game_class.game_cycle(game_stage, win)
        if game_stage[0] == conf.WIN:
            ic.score_class.score_cycle(game_stage, win)
        if game_stage[0] == conf.LOSE:
            ic.score_class.score_cycle(game_stage, win, True)
        if game_stage[0] == conf.PAUSE:
            ic.pause_class.pause_cycle(game_stage, win)
        pass


if __name__ == "__main__":
    ic.menu_class()
    ic.game_class()
    ic.score_class()
    ic.pause_class()
    game_stage = [conf.MENU]
    game()
    pygame.quit()
