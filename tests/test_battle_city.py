import os
import pygame
import pytest
from pygame import event
import game_mech.conf as conf
import game_mech.object_collision as oc
import game_mech.game_classes as gc
import game_mech.building_classes as bc
import game_mech.interface_classes as ic
import game_mech.maps as maps
from game_mech.music import music_class as mc

pygame.init()

player = gc.player_class()
fl_obj = gc.flying_object(player.image)
enemy = gc.enemy_class()
bullet = gc.bullet_class((1, 0), enemy)
platform = bc.cloud_class(100, 100)
battleBase = bc.base_class(0, 100)
exp = gc.explosion_class()


class Test_bullets:
    def test_bul_ind_col(self):
        oc.bullet_group.add(bullet)
        oc.indestructible_platform_group.add(platform)
        oc.indestructible_platform_bullet_collide()
        assert (len(oc.bullet_group) == 0)
        assert (len(oc.indestructible_platform_group) == 1)
        oc.indestructible_platform_group.remove(platform)

    def test_bul_br_block_col(self):
        oc.bullet_group.add(bullet)
        oc.platform_group.add(bc.cloud_class(100, 100))
        oc.platform_bullet_collide()
        assert (len(oc.bullet_group) == 0)
        assert (len(oc.platform_group) == 0)

    def test_player_bullet(self):
        oc.bullet_group.add(bullet)
        oc.player_group.add(player)
        oc.enemy_group.add(enemy)
        oc.players_bullet_collide(oc.player_group)
        assert (len(oc.bullet_group) == 0)
        assert (len(oc.player_group) == 1)
        assert (player.health == conf.player_health - conf.bullet_damage)

    def test_bullet_col(self):
        oc.bullet_group.add(bullet)
        oc.bullet_group.add(gc.bullet_class((1, 0), enemy))
        oc.bullets_collide()
        assert (len(oc.bullet_group) == 0)


class Test_player:
    def test_pl_platf_col(self):
        oc.platform_group.add(bc.cloud_class(100, 100))
        assert (len(oc.platform_group) == 1)
        oc.player_platform_collide(player)
        i_s = conf.image_size // 2
        for direction, position in [((0, 1), (100, 100 - i_s * 2)),
                                    ((0, -1), (100, 100 + i_s)),
                                    ((1, 0), (100 - i_s * 2, 100)),
                                    ((-1, 0), (100 + i_s, 100))]:
            Test_player.dir_tets(direction, position)
            assert (player.rect.x == position[0])
            assert (player.rect.y == position[1])

    def dir_tets(direction, position):
        player.rect.x, player.rect.y = 100, 100
        player.direction = direction
        oc.player_platform_collide(player)

    def test_pl_bon_col(self):
        global player
        player.rect.x, player.rect.y = 100, 100
        oc.player_group.add(player)
        oc.bonus_group.add(bc.bonus(100, 100, player.image, (10, 0, 0)))
        oc.player_bonus_collide()
        assert (player.hearts == 12)
        player = gc.player_class()


class Test_map:
    def test_map(self):
        map_str = str(maps.get_map())
        assert (map_str[:26] == '00000000000000004000000000')

    def test_generation(self):
        map = maps.generate_map()
        assert (len(oc.bullet_group) == 0)
        assert (len(oc.enemy_group) == 6)
        assert (len(oc.platform_group) == 737)
        assert (len(oc.indestructible_platform_group) == 0)

    def test_save_load(self):
        num = maps.save_game()
        maps.load_game(num)
        os.remove(os.path.join(maps.project_path, 'saves', str(num)))

    def test_map_count(self):
        count = maps.get_maps_count()
        assert (count == 5)

    def test_clear(self):
        maps.clear_map()
        assert (len(oc.bullet_group) == 0)
        assert (len(oc.enemy_group) == 0)
        assert (len(oc.platform_group) == 0)
        assert (len(oc.indestructible_platform_group) == 0)


class Test_game_cl:
    dic = gc.tuple_to_int
    oc.enemy_group.add(enemy)
    oc.bullet_group.add(bullet)

    def test_enemy_dir(self):
        enemy.rect.x, enemy.rect.y = 100, 100
        enemy.tick = 901
        enemy.direction = conf.up
        player.rect.x, player.rect.y = 200, 100
        oc.player_group.add(player)
        oc.base_group.add(battleBase)
        enemy.set_direction()
        assert (enemy.direction == conf.right)
        enemy.tick = 1801
        enemy.direction = conf.up
        enemy.set_direction()
        assert (enemy.direction == conf.left)
        enemy.set_aim_direction(player)
        for i in range(5):
            enemy.set_random_direction()
        enemy.enemy_move()
        gc.enemy_class.update_enemy_condition()

    def test_player_move(self):
        keys = pygame.key.get_pressed()
        player.player_move()
        player.check_dir_collision(conf.up)
        gc.player_class.update_player_condition()
        assert (player.rect.y == 100)

    def test_enemy_sp(self):
        enemy.enemy_shoot()
        enemy.move()
        enemy.update_enemy_move()

    def test_exp(self):
        gc.explosion_class.update_exp_condition()
        explosions = [(100, 100)]
        gc.explosion_class.add_exp(explosions)

    def test_bul(self):
        bullet.move()
        gc.bullet_class.update_bullet_move()

    def test_main(self):
        gc.the_time_has_come(player)
        pass

    def test_sign(self):
        assert (gc.enemy_class.sign(-20) == -1)
        assert (gc.enemy_class.sign(20) == 1)


class Test_bonus:
    def test_bonus(self):
        bc.bonus.bonuses_position.extend([(0, 0), (10, 0), (20, 0)])
        bc.bonus.bonus_spawn(True)
        bc.bonus.bonus_spawn(True)
        assert (len(oc.bonus_group) == 3)
        assert (len(bc.bonus.bonuses_position) == 0)


game_stage = [conf.GAME]


class Test_int_game:
    game = ic.game_class()

    def test_butt_press_quit(self):
        game_stage[0] = conf.GAME
        ic.game_class.event_handler(game_stage,
                                    [event.Event(pygame.QUIT)])
        assert (game_stage[0] == conf.END)

    def test_butt_press_quit(self):
        game = Test_int_game.game
        game_stage[0] = conf.GAME
        ic.game_class.event_handler(game_stage,
                                    [event.Event(pygame.MOUSEBUTTONDOWN)],
                                    (game.buttons[2].x,
                                     game.buttons[2].y))
        assert (game_stage[0] == conf.END)

    def test_butt_press_nextlvl(self):
        game = Test_int_game.game
        game_stage[0] = conf.GAME
        ic.game_class.event_handler(game_stage,
                                    [event.Event(pygame.MOUSEBUTTONDOWN)],
                                    (game.buttons[1].x,
                                     game.buttons[1].y))
        assert (game_stage[0] == conf.WIN)

    def test_butt_press_USE(self):
        game_stage[0] = conf.GAME
        ic.game_class.event_handler(game_stage,
                                    [event.Event(pygame.USEREVENT)])
        assert (game_stage[0] == conf.LOSE)

    def test_main(self):
        game_stage[0] = conf.GAME
        player.rect.x, player.rect.y = 100, 100
        player.health = 0
        bullet.rect.x, bullet.rect.y = 100, 100
        maps.clear_map()
        oc.enemy_group.add(enemy)
        oc.player_group.add(player)
        oc.bullet_group.add(bullet)
        ic.game_class.update_condition(game_stage)
        assert ((bullet.rect.x, bullet.rect.y) == (110, 100))
        assert (game_stage[0] == conf.GAME)
        assert (len(oc.bullet_group) == 0)

    def test_draw(self):
        ic.game_class.game_draw(ic.window_class())


class Test_int_menu:
    menu = ic.menu_class()

    def test_menu_button_start(self):
        menu = Test_int_menu.menu
        game_stage[0] = conf.MENU
        ic.menu_class.event_handler(game_stage,
                                    [event.Event(pygame.MOUSEBUTTONDOWN)],
                                    (menu.buttons[0].x,
                                     menu.buttons[0].y))
        assert (game_stage[0] == conf.GAME)

    def test_menu_button_exit(self):
        menu = Test_int_menu.menu
        game_stage[0] = conf.MENU
        ic.menu_class.event_handler(game_stage,
                                    [event.Event(pygame.MOUSEBUTTONDOWN)],
                                    (menu.buttons[1].x,
                                     menu.buttons[1].y))
        assert (game_stage[0] == conf.END)

    def test_draw(self):
        ic.menu_class.menu_draw(ic.window_class())


class Test_int_score:
    score = ic.score_class()

    def test_score_button_start(self):
        score = Test_int_score.score
        game_stage[0] = conf.WIN
        ic.score_class.event_handler(game_stage, False,
                                     [event.Event(pygame.MOUSEBUTTONDOWN)],
                                     (score.buttons[0].x,
                                      score.buttons[0].y))
        assert (game_stage[0] == conf.GAME)

    def test_score_button_exit(self):
        score = Test_int_score.score
        game_stage[0] = conf.MENU
        ic.score_class.event_handler(game_stage, False,
                                     [event.Event(pygame.MOUSEBUTTONDOWN)],
                                     (score.buttons[1].x,
                                      score.buttons[1].y))
        assert (game_stage[0] == conf.END)
        ic.score_class.event_handler(game_stage, True,
                                     [event.Event(pygame.MOUSEBUTTONDOWN)])

    def test_heart(self):
        ic.heart_draw(ic.window_class())
        ic.score_class.score_draw(ic.window_class(), True)
        ic.score_class.score_draw(ic.window_class(), False)


class Test_music:
    def test_update(self):
        mc.update_music(game_stage)


if __name__ == '__main__':
    maps.save_game()
    pytest.main()
