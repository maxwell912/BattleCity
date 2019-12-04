import random
from game_mech import conf
from game_mech import images as im
from game_mech import object_collision as oc

pygame = conf.pygame
Sprite = pygame.sprite.Sprite

tuple_to_int = {
    (0, 1): 0,
    (1, 1): 0,
    (0, -1): 3,
    (-1, -1): 3,
    (-1, 0): 1,
    (1, 0): 2, }


def the_time_has_come(player):
    return player.passed_time >= player.reload_time


image_size = conf.image_size


class flying_object(Sprite):
    """Двигающийся объект"""

    def __init__(self, image, x=100, y=100,
                 direction=(0, 1), size=image_size):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.size = size
        self.direction = direction
        Sprite.__init__(self)


class player_class(flying_object):
    """Класс игрока"""
    start_position = (0, 0)
    hearts = conf.player_heart_count
    score = 0

    def __init__(self, x=100, y=100,
                 animation_sprites=im.dragon_sprites,
                 speed=conf.default_speed,
                 health=conf.player_health,
                 size=image_size,
                 direction=(0, 1)):
        flying_object.__init__(
            self, animation_sprites[tuple_to_int[direction]],
            x, y, direction,  size)
        self.animation = animation_sprites
        self.can_shoot = True
        self.passed_time = conf.reload_time_default
        self.reload_time = conf.reload_time_default
        self.can_change_direction = True
        self.speed = speed
        self.health = health

    def player_move(self):
        """Нажатие клавиш и движение"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            self.check_dir_collision(conf.down)

        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
            self.check_dir_collision(conf.up)

        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
            self.check_dir_collision(conf.right)

        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
            self.check_dir_collision(conf.left)

        if keys[pygame.K_SPACE]:
            if self.passed_time >= self.reload_time:
                oc.bullet_group.add(bullet_class(
                    self.direction, player_class, self.rect.x + 4,
                    self.rect.y + 4, speed=conf.bullet_speed))
                self.passed_time = 0
                pass
        self.passed_time += 1

    def check_dir_collision(self, direction):
        """Столкновение игрока с блоками"""
        self.direction = direction
        self.image = self.animation[tuple_to_int[direction]]
        oc.player_platform_collide(self)
        oc.player_platform_collide(self, oc.base_group)
        oc.player_platform_collide(self, oc.indestructible_platform_group)
        oc.player_platform_collide(self, oc.water_group)
        oc.player_platform_collide(self, oc.enemy_group)

    @staticmethod
    def update_player_condition(players=oc.player_group):
        """Движение игрока"""
        players.sprite.player_move()
        oc.player_bonus_collide()
        pass


class enemy_class(flying_object):
    """Класс врага"""
    score = 0

    def __init__(self, x=100, y=100,
                 animation_sprites=im.rus_sprites,
                 speed=conf.default_speed,
                 health=conf.enemy_health,
                 size=image_size,
                 direction=(0, 1),
                 enemy_num=0):
        flying_object.__init__(
            self, animation_sprites[tuple_to_int[direction]],
            x, y, direction,  size)
        self.animation_sprites = animation_sprites
        self.enemy_num = enemy_num
        self.can_shoot = True
        self.can_change_direction = True
        self.dir_passed_time = 25
        self.dir_reload_time = 25
        self.shoot_passed_time = conf.reload_time_default
        self.shoot_reload_time = conf.reload_time_default
        self.speed = speed
        self.health = health
        self.tick = 0

    def enemy_spawn(self, enemy_num=-1):
        """Задает характеристики врага"""
        if enemy_num == -1:
            enemy_num = random.randint(0, 2)
        if enemy_num == 0:
            return
        elif enemy_num == 2:
            self.enemy_num = 2
            self.animation_sprites = im.siren_sprites
            self.speed = conf.default_speed - 3
            self.health = conf.enemy_health + 50
        elif enemy_num == 1:
            self.enemy_num = 1
            self.animation_sprites = im.bat_sprites
            self.speed = conf.default_speed + 3
            self.health = conf.enemy_health - 50
        pass

    def move(self):
        """Движение врага в выбранном направлении"""
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

    def enemy_move(self):
        """Движение врага"""
        if self.tick < 1800:
            self.tick += 1
        if self.dir_passed_time >= self.dir_reload_time:
            self.dir_passed_time = 0
            self.set_direction()
            self.can_change_direction = False
        self.move()
        self.dir_passed_time += 1

    def update_enemy_move(self):
        """Столкновение врага с объектами"""
        self.enemy_move()
        oc.player_platform_collide(self, oc.player_group)
        oc.player_platform_collide(self, oc.base_group)
        oc.player_platform_collide(self, oc.enemy_group)
        oc.player_platform_collide(self)
        oc.player_platform_collide(self, oc.water_group)
        oc.player_platform_collide(self, oc.indestructible_platform_group)

    def enemy_shoot(self):
        """Стрельба"""
        if self.shoot_passed_time >= self.shoot_reload_time:
            oc.bullet_group.add(bullet_class(self.direction,
                                             enemy_class,
                                             self.rect.x + 4,
                                             self.rect.y + 4,
                                             speed=12 - self.speed))
            self.shoot_passed_time = 0
        self.shoot_passed_time += 1

    def update_enemy_condition(enemies=oc.enemy_group):
        """Действия врага во время игры"""
        for enemy in enemies:
            enemy.update_enemy_move()
            enemy.enemy_shoot()
        pass

    def set_direction(self):
        if self.tick < 900:
            self.set_random_direction()
        elif self.tick < 1800:
            self.set_aim_direction(oc.player_group.sprite)
        else:
            self.set_aim_direction(oc.base_group.sprite)
        self.image = self.animation_sprites[tuple_to_int[self.direction]]

    def set_random_direction(self):
        """Выбор случайного направления"""
        rand_num = random.randint(0, 2)
        if rand_num == 0:
            self.direction = conf.right
        elif rand_num == 1:
            self.direction = conf.left
        elif rand_num == 2:
            self.direction = conf.up
        else:
            self.direction = conf.down

    def set_aim_direction(self, aim):
        if aim is not None:
            aim_cord = (aim.rect.x, aim.rect.y)
            enemy_direction = (aim_cord[0] - self.rect.x,
                               aim_cord[1] - self.rect.y)
            dir = self.direction
            ec = enemy_class
            if dir == conf.right or dir == conf.left:
                self.direction = (0, ec.sign(enemy_direction[1]))
            else:
                self.direction = (ec.sign(enemy_direction[0]), 0)
        pass

    @staticmethod
    def sign(number):
        if number >= 0:
            return 1
        return -1


class bullet_class(flying_object):
    """Класс пули"""

    def __init__(self, direction=(0, 0), parent=enemy_class, x=100, y=100,
                 speed=10, size=image_size):
        super().__init__(im.bullet_image, x, y, direction, size)
        self.speed = speed
        self.direction = direction
        self.parent = parent

    def move(self):
        """Движение пули"""
        self.rect.x += self.direction[0] * self.speed
        self.rect.y += self.direction[1] * self.speed

    @staticmethod
    def update_bullet_move(bullets=oc.bullet_group,
                           clouds=oc.platform_group):
        """Движение и попадание"""
        for bullet in bullets:
            bullet.move()
            rect = bullet.rect
            win_height = conf.win_height
            check_hor = rect.y > win_height or rect.y < 0
            check_vert = rect.x > win_height or rect.x < 0
            if check_hor or check_vert:
                oc.bullet_group.remove(bullet)

        explosions = oc.players_bullet_collide(
            oc.player_group)
        explosions.extend(oc.players_bullet_collide(
            oc.enemy_group))
        explosion_class.add_exp(explosions)
        oc.platform_bullet_collide()
        oc.indestructible_platform_bullet_collide()
        oc.bullets_collide()


class explosion_class(Sprite):
    def __init__(self, x=100, y=100, image=im.explosion_image,
                 size=image_size):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.size = size
        self.time = 17
        Sprite.__init__(self)

    @staticmethod
    def add_exp(explosions):
        for exp in explosions:
            oc.effects_group.add(explosion_class(*exp))

    @staticmethod
    def update_exp_condition():
        for exp in oc.effects_group:
            exp.time -= 1
            if exp.time == 0:
                oc.effects_group.remove(exp)
