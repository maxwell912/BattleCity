import os

import game_mech.building_classes as build
import game_mech.maps as m
from game_mech import conf
from game_mech import images as im
from game_mech.conf import menu_start, menu_exit
from game_mech.conf import win_height, win_width, image_size
from game_mech.game_classes import bullet_class, explosion_class
from game_mech.game_classes import oc
from game_mech.game_classes import player_class, enemy_class

pygame = conf.pygame

pygame.font.init()


class button_class:
    """Кнопка"""

    def __init__(self, function, image, x=0, y=0, height=0, width=0):
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.image = image
        self.function = function

    def on_click(self, position):
        """Проверка нажатия на кнопку"""
        first_cord = self.x + self.width >= position[0] >= self.x
        sec_cord = self.y + self.height >= position[1] >= self.y
        return first_cord and sec_cord

    def draw(self, win):
        self.image.get_rect()
        win.blit(self.image, (self.x, self.y))
        if type(win) is not window_class:
            pygame.draw.rect(win, (255, 255, 0),
                             (self.x, self.y, self.width, self.height), 1)


class menu_class:
    """Класс описывающий работу меню игры"""
    buttons = list()

    def __init__(self):

        menu_class.buttons.append(button_class(menu_class.start_button,
                                               im.start_button,
                                               menu_start[0], menu_start[1],
                                               100, 250))

        menu_class.buttons.append(button_class(menu_class.end_button,
                                               im.quit_button,
                                               menu_exit[0], menu_exit[1],
                                               100, 250))

    @staticmethod
    def start_button(game_stage):
        m.generate_map()
        game_stage[0] = conf.GAME

    @staticmethod
    def end_button(game_stage):
        game_stage[0] = conf.END

    @staticmethod
    def menu_update(win):
        """Прорисовывает все элементы меню"""
        pygame.display.update()
        menu_class.menu_draw(win)

    @staticmethod
    def menu_draw(win):
        win.blit(im.menu_fon, (0, 0))
        for button in menu_class.buttons:
            win.blit(button.image, (button.x, button.y))

    @staticmethod
    def event_handler(game_stage, events=None, position=None):
        """Обрабатывает события"""
        if events is None:
            events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_stage[0] = conf.END
            if event.type == pygame.MOUSEBUTTONDOWN:
                if position is None:
                    position = pygame.mouse.get_pos()
                for button in menu_class.buttons:
                    if button.on_click(position):
                        button.function(game_stage)
                pass
            pass

    @staticmethod
    def menu_cycle(game_stage, win):
        """Обрабатывает нажатия и прорисовывает"""
        menu_class.event_handler(game_stage)
        menu_class.menu_update(win)


class game_class:
    buttons = list()
    button_size = (50, 250)
    myfont = pygame.font.SysFont('Comic Sans MS', 40)

    def __init__(self):
        gc = game_class
        gc.buttons.append(button_class(gc.pause_button,
                                       gc.myfont.render('Pause',
                                                        False,
                                                        (255, 255, 0)),
                                       win_width - gc.button_size[1],
                                       win_height - 300,
                                       gc.button_size[0],
                                       gc.button_size[1]))

        gc.buttons.append(button_class(gc.next_lvl_button,
                                       gc.myfont.render('Next level',
                                                        False,
                                                        (255, 255, 0)),
                                       win_width - gc.button_size[1],
                                       win_height - 200,
                                       gc.button_size[0],
                                       gc.button_size[1]))

        gc.buttons.append(button_class(gc.end_button,
                                       gc.myfont.render('Exit',
                                                        False,
                                                        (255, 255, 0)),
                                       win_width - gc.button_size[1],
                                       win_height - 100,
                                       gc.button_size[0],
                                       gc.button_size[1]))

    @staticmethod
    def next_lvl_button(game_stage):
        game_stage[0] = conf.WIN

    @staticmethod
    def end_button(game_stage):
        game_stage[0] = conf.END

    @staticmethod
    def pause_button(game_stage):
        game_stage[0] = conf.PAUSE

    @staticmethod
    def game_cycle(game_stage, win):
        """Реализует игровой процесс и обрабатывает нажатия"""
        game_class.event_handler(game_stage)
        game_class.update_condition(game_stage)
        game_class.game_win_update(game_stage, win)

    @staticmethod
    def event_handler(game_stage, events=None, position=None):
        """Обрабатывает события"""
        if events is None:
            events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_stage[0] = conf.END
            if event.type == pygame.USEREVENT:
                game_stage[0] = conf.LOSE
            if event.type == pygame.MOUSEBUTTONDOWN:
                if position is None:
                    position = pygame.mouse.get_pos()
                for button in game_class.buttons:
                    if button.on_click(position):
                        button.function(game_stage)
        pass

    @staticmethod
    def game_win_update(game_stage, win):
        """Реализует игровой процесс"""
        pygame.display.update()
        game_class.game_draw(win)

    @staticmethod
    def update_condition(game_stage):
        """Обновляет состояние игровых элементов"""
        player_class.update_player_condition()
        enemy_class.update_enemy_condition()
        bullet_class.update_bullet_move()
        explosion_class.update_exp_condition()
        build.base_class.update_base_cond()
        build.bonus.bonus_spawn()
        if len(oc.enemy_group.sprites()) == 0:
            game_stage[0] = conf.WIN
        if len(oc.player_group.sprites()) == 0:
            if player_class.hearts > 0:
                oc.player_group.add(player_class(
                    *player_class.start_position))
                player_class.hearts -= 1
            else:
                game_stage[0] = conf.LOSE
        pass

    @staticmethod
    def game_draw(win):
        """Прорисовывает элементы игры"""
        win.fill((20, 68, 108))
        win.blit(im.battle_field_image, (0, 0))
        for button in game_class.buttons:
            button.draw(win)

        for group in m.groups:
            group.draw(win)

        heart_draw(win)


class pause_class:
    buttons = list()
    button_size = (50, 250)

    def __init__(self):
        pc = pause_class
        myfont = pygame.font.SysFont('Comic Sans MS', 20)
        for i in os.listdir('saves'):
            k = int(i)
            if k > 47:
                break
            image = myfont.render(i, False, (255, 255, 0))
            pc.buttons.append(button_class(pc.load_button(k),
                                           image,
                                           (k // 24) * 300, (k % 24) * 26,
                                           24, 300))
        myfont = pygame.font.SysFont('Comic Sans MS', 40)
        pc.buttons.append(button_class(pc.continue_button,
                                       # im.continue_button,
                                       myfont.render('Continue', False,
                                                     (255, 255, 0)),
                                       win_width - pc.button_size[1],
                                       win_height - 300,
                                       pc.button_size[0],
                                       pc.button_size[1]))

        pc.buttons.append(button_class(pc.save_button,
                                       # im.save_button,
                                       myfont.render('Save', False,
                                                     (255, 255, 0)),
                                       win_width - pc.button_size[1],
                                       win_height - 200,
                                       pc.button_size[0],
                                       pc.button_size[1]))

        pc.buttons.append(button_class(pc.end_button,
                                       # im.exit_image,
                                       myfont.render('Exit', False,
                                                     (255, 255, 0)),
                                       win_width - pc.button_size[1],
                                       win_height - 100,
                                       pc.button_size[0],
                                       pc.button_size[1]))

    @staticmethod
    def load_button(number):
        num = number
        return lambda game_stage: m.load_game(num)

    @staticmethod
    def save_button(game_stage):
        game_stage[0] = conf.PAUSE
        num = len(os.listdir('saves'))
        if num > 47:
            return
        m.save_game()
        myfont = pygame.font.SysFont('Comic Sans MS', 20)
        image = myfont.render(str(num), False, (255, 255, 0))
        pause_class.buttons.append(button_class(pause_class.load_button(num),
                                                image,
                                                (num // 24) * 300,
                                                (num % 24) * 26,
                                                24, 300))

    @staticmethod
    def end_button(game_stage):
        game_stage[0] = conf.END

    @staticmethod
    def continue_button(game_stage):
        game_stage[0] = conf.GAME

    @staticmethod
    def pause_cycle(game_stage, win):
        pygame.display.update()
        pause_class.event_handler(game_stage)
        pause_class.pause_draw(win)

    @staticmethod
    def pause_draw(win):
        win.blit(im.menu_fon, (0, 0))
        for button in pause_class.buttons:
            button.draw(win)

    @staticmethod
    def event_handler(game_stage, events=None, position=None):
        if events is None:
            events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_stage[0] = conf.END
            if event.type == pygame.MOUSEBUTTONDOWN:
                if position is None:
                    position = pygame.mouse.get_pos()
                for button in pause_class.buttons:
                    if button.on_click(position):
                        game_stage[0] = conf.GAME
                        button.function(game_stage)


class score_class:
    """Реализует обновление уровня"""
    buttons = list()
    button_size = (50, 250)
    myfont = pygame.font.SysFont('Comic Sans MS', 40)
    game_win = None
    game_lose = None

    def __init__(self):
        sc = score_class
        sc.game_win = sc.myfont.render('Уровень пройден', False, (255, 255, 0))
        sc.game_lose = sc.myfont.render('Игра проиграна', False, (255, 255, 0))

        sc.buttons.append(button_class(score_class.next_lvl_button,
                                       sc.myfont.render('Next level', False,
                                                        (255, 255, 0)),
                                       win_width - sc.button_size[1],
                                       win_height - 200,
                                       sc.button_size[0],
                                       sc.button_size[1]))

        sc.buttons.append(button_class(sc.end_button,
                                       sc.myfont.render('Exit', False,
                                                        (255, 255, 0)),
                                       win_width - sc.button_size[1],
                                       win_height - 100,
                                       sc.button_size[0],
                                       sc.button_size[1]))

    @staticmethod
    def next_lvl_button(*args):
        game_stage = args[0]
        is_lost = args[1]
        if is_lost:
            conf.level_num[0] = 1
        m.clear_map()
        if m.generate_map():
            game_stage[0] = conf.MENU
        else:
            game_stage[0] = conf.GAME

    @staticmethod
    def end_button(*args):
        game_stage = args[0]
        game_stage[0] = conf.END

    @staticmethod
    def score_cycle(game_stage, win, is_lost=False):
        pygame.display.update()
        score_class.score_draw(win, is_lost)
        score_class.event_handler(game_stage, is_lost)

    @staticmethod
    def event_handler(game_stage, is_lost, events=None, position=None):
        """Обрабатывает события"""
        if events is None:
            events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                game_stage[0] = conf.END
            if event.type == pygame.MOUSEBUTTONDOWN:
                if position is None:
                    position = pygame.mouse.get_pos()
                for button in score_class.buttons:
                    if button.on_click(position):
                        button.function(game_stage, is_lost)
            pass

    @staticmethod
    def score_draw(win, is_lost):
        """Отрисовывает счет"""
        sc = score_class
        win.blit(im.menu_fon, (0, 0))
        if is_lost:
            win.blit(sc.game_lose,
                     (win_width // 4, win_height // 4))
        else:
            win.blit(sc.game_win,
                     (win_width // 4 - 40, win_height // 4))
            if m.level_num[0] == m.maps_count + 1:
                win.blit(sc.myfont.render('Вы прошли игру',
                                          False,
                                          (255, 255, 0)),
                         (win_width // 4 - 50, win_height // 4 + 250))
        score = sc.myfont.render('Ваш счет ' + str(player_class.score),
                                 False,
                                 (255, 255, 0))
        win.blit(score,
                 (win_width // 4, win_height // 4 + 100))
        for button in score_class.buttons:
            button.draw(win)


class window_class:
    def blit(self, image, position):
        pass

    def fill(self, color):
        pass


def heart_draw(win):
    """Прорисовывает иконку жизней игрока"""
    heart_count = player_class.hearts
    if oc.player_group.sprite is not None:
        for i in range(heart_count):
            win.blit(im.heart_image, (win_height + i * image_size * 2, 0))
        if len(oc.player_group) == 1:
            if oc.player_group.sprite.health == 100:
                win.blit(im.heart_image,
                         (win_height + heart_count * image_size * 2, 0))
            else:
                win.blit(im.heart_half_image,
                         (win_height + heart_count * image_size * 2, 0))
    pass
