import os
from os.path import join, dirname

from game_mech.game_classes import player_class, enemy_class
from game_mech.game_classes import bullet_class
from game_mech.game_classes import oc as c
from game_mech import building_classes as bc
from game_mech.conf import model_height, model_width
from game_mech.conf import level_num, player_heart_count
from game_mech import images as im

project_path = dirname(__file__)[:-9]

groups = [c.platform_group,
          c.indestructible_platform_group,
          c.base_group,
          c.water_group,
          c.enemy_group,
          c.player_group,
          c.bullet_group,
          c.hide_platform_group,
          c.bonus_group,
          c.effects_group]


def get_map():
    """Получает из файла новую карту"""
    file = join(project_path, "levels", str(level_num[0]))
    level_num[0] += 1
    return open(file, 'r').read()


def get_maps_count():
    return len(os.listdir(join(project_path, "levels")))


maps_count = get_maps_count()


def clear_map():
    """Удаляет все объекты карты"""
    for group in groups:
        group.empty()
    bc.bonus.bonuses_position.clear()
    player_class.hearts = player_heart_count


def generate_map():
    """Генерирует новую карту"""
    if level_num[0] == maps_count + 1:
        level_num[0] = 1
        return True
    map = get_map().split('\n')
    for col in range(26):
        for row in range(26):
            map_sprite = map[col][row]
            if map_sprite == '2':
                for i in range(2):
                    for j in range(2):
                        c.platform_group.add(bc.cloud_class(
                            row * model_width + i * model_width // 2,
                            col * model_height + j * model_width // 2))
            elif map_sprite == '3':
                c.indestructible_platform_group.add(bc.cloud_class(
                    row * model_width, col * model_height,
                    im.indestr_block))
            elif map_sprite == '4':
                enemy = enemy_class(row * model_width,
                                    col * model_height)
                enemy.enemy_spawn()
                c.enemy_group.add(enemy)
            elif map_sprite == '6':
                c.player_group.add(player_class(
                    row * model_width, col * model_height,
                    im.dragon_sprites))
                player_class.start_position = (
                    row * model_width, col * model_height)
            elif map_sprite == '9':
                c.base_group.add(
                    bc.base_class(row * model_width, col * model_height,
                                  im.base_image))
            elif map_sprite == '5':
                c.hide_platform_group.add(bc.hide_block(
                    row * model_width, col * model_height,
                    im.hide_block_image))
            elif map_sprite == '1':
                c.water_group.add(bc.water_block(row * model_width,
                                                 col * model_height,
                                                 im.water_block_image))
            elif map_sprite == '7':
                bc.bonus.bonuses_position.append(
                    (row * model_width, col * model_height))
    pass


def save_game():
    group_to_num = {
        groups[0]: 0,
        groups[1]: 1,
        groups[2]: 2,
        groups[3]: 3,
        groups[4]: 4,
        groups[5]: 5,
        groups[6]: 6,
        groups[7]: 7}
    next_save_num = 0
    if len(os.listdir(path=join(project_path, 'saves'))) > 0:
        next_save_num = int(sorted(os.listdir(
								   path=join(project_path, 'saves')),
                                   key=lambda val: int(val))[-1]) + 1
    with open(join(project_path, 'saves',
			  str(next_save_num)), 'xb') as save_file:
        save_file.write(bytes([level_num[0]]))
        for group in groups[:-2]:
            sprites = group.sprites()
            sprites_count = len(sprites)
            for i in range(sprites_count):
                sprite = sprites[i]
                if i % 255 == 0:
                    save_file.write(bytes([group_to_num[group],
                                           min(sprites_count - i, 255)]))
                save_file.write(
                    bytes([sprite.rect.x // 4, sprite.rect.y // 4]))
                if group is c.enemy_group:
                    save_file.write(bytes([sprite.enemy_num]))
                elif group is c.player_group:
                    save_file.write(bytes([player_class.hearts]))
                elif group is c.bullet_group:
                    par_num = 1 if type(sprite) == enemy_class else 0
                    save_file.write(bytes([sprite.direction[0] + 1,
                                           sprite.direction[1] + 1,
                                           par_num]))
    return next_save_num


def load_game(save_num):
    group_to_mem = {
        groups[0]: bc.cloud_class,
        groups[1]: bc.rock_class,
        groups[2]: bc.base_class,
        groups[3]: bc.water_block,
        groups[4]: enemy_class,
        groups[5]: player_class,
        groups[6]: bullet_class,
        groups[7]: bc.hide_block}

    def next_int(file):
        return int.from_bytes(file.read(1), 'little')

    with open(join(project_path, 'saves', str(save_num)), 'rb') as load_file:
        clear_map()
        level_num[0] = next_int(load_file)
        while True:
            group_byte = load_file.read(1)
            if group_byte == b'':
                break
            group = groups[int.from_bytes(group_byte, 'little')]
            for i in range(next_int(load_file)):
                gr_member = group_to_mem[group](x=next_int(load_file) * 4,
                                                y=next_int(load_file) * 4)
                if group is c.enemy_group:
                    enemy_num = next_int(load_file)
                    gr_member.enemy_spawn(enemy_num)
                elif group is c.player_group:
                    player_class.hearts = next_int(load_file)
                elif group is c.bullet_group:
                    gr_member.direction = (next_int(load_file) - 1,
                                           next_int(load_file) - 1)
                    gr_member.parent = enemy_class
                    if next_int(load_file) == 0:
                        gr_member.parent = player_class
                group.add(gr_member)
