from game_mech import conf
from game_mech.images import cloud_destruction

pygame = conf.pygame
sprite = pygame.sprite


player_group = sprite.GroupSingle()
base_group = sprite.GroupSingle()

enemy_group = sprite.Group()
bullet_group = sprite.Group()
platform_group = sprite.Group()
indestructible_platform_group = sprite.Group()
hide_platform_group = sprite.Group()
water_group = sprite.Group()
bonus_group = sprite.Group()
effects_group = sprite.Group()


def indestructible_platform_bullet_collide(
        platforms=indestructible_platform_group, bullets=bullet_group):
    """Попадание пули в неразр. блок"""
    sprite.groupcollide(platforms, bullets, 0, 1)


def player_platform_collide(player, platforms=platform_group):
    """Взаимодействие игрока и блоков"""
    for platform in sprite.spritecollide(player, platforms, False):
        if player != platform:
            set_border(player, platform)
            player.can_change_direction = True
    check_field_overlimit(player)


def set_border(player, barrier):
    if player.direction == conf.up:
        player.rect.top = barrier.rect.bottom
    elif player.direction == conf.down:
        player.rect.bottom = barrier.rect.top
    elif player.direction == conf.left:
        player.rect.left = barrier.rect.right
    else:
        player.rect.right = barrier.rect.left


def check_field_overlimit(player):
    """Проверка на выход за границы карты"""
    if player.rect.y > conf.win_height - player.size:
        player.rect.y = conf.win_height - player.size

    if player.rect.y < 0:
        player.rect.y = 0

    if player.rect.x > conf.win_height - player.size:
        player.rect.x = conf.win_height - player.size

    if player.rect.x < 0:
        player.rect.x = 0
    pass


def players_bullet_collide(players, bullets=bullet_group):
    """Взаимодействие игрока и пуль"""
    explosions = []
    for player, bullets in sprite.groupcollide(players,
                                               bullets, 0, 0).items():
        for bullet in bullets:
            if bullet.parent != type(player):
                explosions.append(player.rect.topleft)
                player.health -= conf.bullet_damage
                if player.health <= 0:
                    bullet.parent.score += 100
                    players.remove(player)
                bullet_group.remove(bullet)
    return explosions


def platform_bullet_collide(platforms=platform_group,
                            bullets=bullet_group):
    """Взаимодействие пуль и блоков"""
    for bullet, platforms in sprite.groupcollide(
            bullets, platforms, 1, 1).items():
        for platform in platforms:
            if bullet.direction == conf.down:
                change_image(platform, conf.down, 0, 0.5)
            elif bullet.direction == conf.up:
                change_image(platform, conf.up, 0, 0)
            elif bullet.direction == conf.left:
                change_image(platform, conf.left, 0, 0)
            else:
                change_image(platform, conf.right, 0.5, 0)


def change_image(platform, direction, k_hor, k_ver):
    """Анимирует разрушение блока"""
    image_rect = platform.image.get_rect().size
    cord = (platform.rect.x, platform.rect.y)
    quatre_size = (conf.image_size // 2, conf.image_size // 2)
    if image_rect != quatre_size:
        platf_image = cloud_destruction[(image_rect, direction)]
    else:
        platf_image = None
    if platf_image is not None:
        platform.image = platf_image
        platform.rect = platform.image.get_rect()
        platform.rect.x = int(cord[0] + conf.image_size * k_hor)
        platform.rect.y = int(cord[1] + conf.image_size * k_ver)
        platform_group.add(platform)
    pass


def bullets_collide(bullets=bullet_group):
    """Взаимодействие пуль"""
    for bullet1, bullets in sprite.groupcollide(
            bullets, bullets, 0, 0).items():
        for bullet2 in bullets:
            if bullet2 != bullet1:
                bullet_group.remove(bullet2)
                bullet_group.remove(bullet1)
    pass


def base_bullets_collide(bases=base_group, bullets=bullet_group):
    """Взаимодействие пуль и базы"""
    if len(sprite.groupcollide(bases, bullets, 1, 1).keys()) != 0:
        pygame.event.post(pygame.event.Event(pygame.USEREVENT))
    pass


def player_bonus_collide():
    """Взаимодействие игрока и бонусов"""
    for player, bonuses in sprite.groupcollide(
            player_group, bonus_group, 0, 1).items():
        for bonus in bonuses:
            type(bonus).bonuses_position.append(bonus.rect.topleft)
            effect = bonus.effect
            if type(player).hearts < 5:
                type(player).hearts += effect[0]
            if player.speed < 10:
                player.speed += effect[1]
            if player.reload_time > 20:
                player.reload_time += effect[2]
