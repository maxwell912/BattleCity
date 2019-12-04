from os.path import join, dirname
from game_mech.conf import win_width, win_height, image_size
from game_mech.conf import model_width, model_height
from game_mech.conf import up, down, right, left
from game_mech.conf import pygame

image_dir = dirname(__file__)[:-9] + 'images'


def get_animation_sprites(sprite_image):
    sprite_list = []
    sprites = pygame.transform.scale(pygame.image.load(
        sprite_image), [image_size * 4, image_size * 4])
    for i in range(0, 4):
        sprite_list.append(sprites.subsurface(
            0, i * image_size, image_size, image_size))
    return sprite_list


def get_image(file, x, y):
    return pygame.transform.scale(pygame.image.load(file), [x, y])


breaking_block = get_image(
    join(image_dir, "tree.png"), model_width, model_height)
breaking_block_horizontal = breaking_block.subsurface(
    0, 0, image_size, image_size // 2)
breaking_block_vertical = breaking_block.subsurface(
    0, 0, image_size // 2, image_size)
breaking_block_quarter = breaking_block.subsurface(
    0, 0, image_size // 2, image_size // 2)

indestr_block = get_image(join(image_dir, "stone.png"),
                          model_width, model_height)

hide_block_image = get_image(
    join(image_dir, "kek.png"), model_width, model_height)

water_block_image = get_image(
    join(image_dir, "indestr_cloud.png"), model_width, model_height)

base_image = get_image(join(image_dir, "base.png"),
                       model_width * 2, model_height * 2)

sprites = get_image(join(image_dir, "fire.png"),
                    image_size * 5, image_size * 5)
explosion_image = sprites.subsurface(
    4 * image_size, 2 * image_size, image_size, image_size)
bullet_image = sprites.subsurface(
    3 * image_size + 4, 3 * image_size + 4, image_size - 8, image_size - 8)

heart_image = get_image(join(image_dir, "heart.png"),
                        model_width * 2, model_height * 2)
heart_half_image = heart_image.subsurface(
    0, 0, image_size, image_size * 2)
boots_image = get_image(join(image_dir, "boots.png"),
                        model_width, model_height)
heart_bonus_image = get_image(
    join(image_dir, "heart.png"), model_width, model_height)
bullet_bonus_image = get_image(
    join(image_dir, "bullet.png"), model_width, model_height)

dragon_sprites = get_animation_sprites(join(image_dir, "drag.png"))
siren_sprites = get_animation_sprites(join(image_dir, "siren.png"))
bat_sprites = get_animation_sprites(join(image_dir, "bat.png"))
rus_sprites = get_animation_sprites(join(image_dir, "bird.png"))

battle_field_image = get_image(join(
    image_dir, "noch.png"), win_height, win_height)
menu_fon = get_image(join(
    image_dir, "menu_fon.jpg"), win_width, win_height)
start_button = get_image(join(image_dir, "start_button.png"), 250, 100)
quit_button = get_image(join(image_dir, "qiut_button.png"), 250, 100)

cloud_destruction = {
    ((image_size, image_size), up): breaking_block_horizontal,
    ((image_size, image_size), down): breaking_block_horizontal,
    ((image_size, image_size), left): breaking_block_vertical,
    ((image_size, image_size), right): breaking_block_vertical,

    ((image_size, image_size // 2), right): breaking_block_quarter,
    ((image_size, image_size // 2), left): breaking_block_quarter,
    ((image_size, image_size // 2), up): None,
    ((image_size, image_size // 2), down): None,

    ((image_size // 2, image_size), right): None,
    ((image_size // 2, image_size), left): None,
    ((image_size // 2, image_size), up): breaking_block_quarter,
    ((image_size // 2, image_size), down): breaking_block_quarter}
