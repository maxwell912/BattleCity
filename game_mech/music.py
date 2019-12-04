from os.path import join, dirname
from game_mech import conf

mixer = conf.pygame.mixer
project_path = dirname(__file__)[:-9]


class music_class:
    music_stage = -1
    mixer.init(channels=1)
    menu_music = join(project_path, "music", "bensound-birthofahero.mp3")
    game_music = join(project_path, "music", "skyrim_mus.mp3")
    score_music = join(project_path, "music",
                       "bensound-theelevatorbossanova.mp3")

    @staticmethod
    def update_music(game_stage):
        if game_stage != music_class.music_stage:
            music_class.music_stage = game_stage
            if game_stage == conf.MENU:
                music_class.play_menu_mus()
            elif game_stage == conf.GAME:
                music_class.play_game_mus()
            elif game_stage == conf.LOSE or game_stage == conf.WIN:
                music_class.play_score_mus()
            else:
                music_class.play_score_mus()

    @staticmethod
    def play_menu_mus():
        music_class.play_music(music_class.menu_music)

    @staticmethod
    def play_game_mus():
        music_class.play_music(music_class.game_music)

    @staticmethod
    def play_score_mus():
        music_class.play_music(music_class.score_music)

    @staticmethod
    def play_music(music_path):
        mixer.music.stop()
        mixer.music.load(music_path)
        mixer.music.play()
