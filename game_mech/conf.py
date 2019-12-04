import importlib
import sys
import os
sys.path.insert(0, os.path.join("game_mech"))

try:
    pygame = importlib.import_module('pygame')
finally:
    pass

win_width = 1024
win_height = 624
image_size = win_height // 26
FPS = 30

model_width = win_height // 26
model_height = win_height // 26

menu_start = (50, (win_height - 200) // 2)
menu_exit = (50, menu_start[1] + 100)
game_exit = ()

level_num = [1]

down = (0, 1)
up = (0, -1)
right = (1, 0)
left = (-1, 0)

default_speed = 5
bullet_speed = 10
reload_time_default = 45


bullet_damage = 50
enemy_health = 100
player_health = 100
player_heart_count = 2


MENU = 0
GAME = 1
WIN = 2
LOSE = 3
END = 4
PAUSE = 5
