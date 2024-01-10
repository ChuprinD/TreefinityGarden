from tkinter import *

from src.game.game import run_game
from src.menu.achievements_window import run_achievements
from src.objects.player import Player
from src.objects.garden import Garden
from src.objects.window import Window
from src.utilities.json import set_player_default_file
from src.game.tree_generator import run_generator


def open_tree_generator(root):
    root.destroy()
    run_generator(admin=False)


def open_game(root, player):
    root.destroy()
    run_game(player)


def open_achievement_window(root, player):
    root.destroy()
    run_achievements(player)


def run_menu():
    root = Tk()

    WIDTH = 420
    HEIGHT = 720

    buttons = [{'name': 'start',        'x': WIDTH // 2, 'y': HEIGHT * 4 // 9,
                'path_img': 'resources/sprites/buttons/regular_buttons/start.png',        'path_img_under_cursor': 'resources/sprites/buttons/under_cursor_buttons/start.png',
                'command': lambda: open_game(root, player)},
               {'name': 'create_skin',  'x': WIDTH // 2, 'y': HEIGHT * 4 // 9 + HEIGHT // 10,
                'path_img': 'resources/sprites/buttons/regular_buttons/create_skin.png',  'path_img_under_cursor': 'resources/sprites/buttons/under_cursor_buttons/create_skin.png',
                'command': lambda: open_tree_generator(root)},
               {'name': 'achievements', 'x': WIDTH // 2, 'y': HEIGHT * 4 // 9 + HEIGHT // 5,
                'path_img': 'resources/sprites/buttons/regular_buttons/achievements.png', 'path_img_under_cursor': 'resources/sprites/buttons/under_cursor_buttons/achievements.png',
                'command': lambda: open_achievement_window(root, player)},
               {'name': 'reset',        'x': WIDTH // 2, 'y': HEIGHT * 4 // 9 + HEIGHT * 3 // 10,
                'path_img': 'resources/sprites/buttons/regular_buttons/reset.png',        'path_img_under_cursor': 'resources/sprites/buttons/under_cursor_buttons/reset.png',
                'command': lambda: set_player_default_file('resources/players/player.txt', player)}]

    window = Window(root, title='Treefinity Garden', size=[WIDTH, HEIGHT], path_icon='resources/sprites/icon.ico',
                    path_background_img='resources/sprites/backgrounds/window_background.png', buttons=buttons)

    icon = PhotoImage(file='resources/sprites/icon.png')
    window.canvas.create_image(135, 30, anchor='nw', image=icon)

    name_of_project = PhotoImage(file='resources/sprites/project_name.png')
    window.canvas.create_image(25, 210, anchor='nw', image=name_of_project)

    player = Player(name='Player1', garden=Garden())
    player.load()

    root.mainloop()