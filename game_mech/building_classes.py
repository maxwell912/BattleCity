import random
from game_mech import images as im
from pygame.sprite import Sprite
from game_mech.object_collision import base_bullets_collide, bonus_group


class cloud_class(Sprite):
    """Класс блока"""

    def __init__(self, x, y, image=im.breaking_block_quarter):
        Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class rock_class(Sprite):
    """Класс блока"""

    def __init__(self, x, y, image=im.indestr_block):
        Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class base_class(Sprite):
    """Класс базы"""

    def __init__(self, x, y, image=im.base_image):
        Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    @staticmethod
    def update_base_cond():
        """Проверка за уничтожение базы"""
        base_bullets_collide()


class hide_block(Sprite):
    """Класс кустов"""

    def __init__(self, x, y, image=im.hide_block_image):
        Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class water_block(Sprite):
    """Класс воды"""

    def __init__(self, x, y, image=im.water_block_image):
        Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class bonus(Sprite):
    """Класс бонусов"""
    bonus_effects = [(1, 0, 0), (0, 1, 0), (0, 0, -7)]
    # (extra health, speed_bonus, damage_bonus, reload_bonus)
    bonuses_position = []

    def __init__(self, x, y, image, effect):
        Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.effect = effect

    def bonus_spawn(bool_test=False):
        """Появление бонусов"""
        if len(bonus.bonuses_position) != 0:
            rand_num = random.randint(0, 1000)
            if rand_num == 0 or bool_test:
                rand_pos = random.randint(0, len(bonus.bonuses_position) - 1)
                position = bonus.bonuses_position[rand_pos]
                bonus.bonuses_position.remove(position)
                bonus_group.add(bonus(
                    *position,
                    im.heart_bonus_image, bonus.bonus_effects[0]))
            if rand_num == 1 or bool_test:
                rand_pos = random.randint(0, len(bonus.bonuses_position) - 1)
                position = bonus.bonuses_position[rand_pos]
                bonus.bonuses_position.remove(position)
                bonus_group.add(
                    bonus(
                        *position,
                        im.boots_image, bonus.bonus_effects[1]))
            if rand_num == 2 or bool_test:
                rand_pos = random.randint(0, len(bonus.bonuses_position) - 1)
                position = bonus.bonuses_position[rand_pos]
                bonus.bonuses_position.remove(position)
                bonus_group.add(bonus(
                    *position,
                    im.bullet_bonus_image, bonus.bonus_effects[2]))
