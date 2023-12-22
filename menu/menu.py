from tkinter import *

from game.game import run_game
from menu.achievements_window import run_achievements
from objects.window import Window
from utilities.json import set_player_default_file
from tree_generator import run_generator


def close_menu_run_generator(root):
    root.destroy()
    run_generator(admin=False)


def close_menu_run_game(root):
    root.destroy()
    run_game()


def open_achievement_window(root):
    root.destroy()
    run_achievements()


def run_menu():
    root = Tk()

    WIDTH = 420
    HEIGHT = 720

    buttons = [{'x': WIDTH // 2, 'y': HEIGHT * 4 // 9, 'path_img': './sprites/buttons/start_button.png',
                'command': lambda: close_menu_run_game(root)},
               {'x': WIDTH // 2, 'y': HEIGHT * 4 // 9 + HEIGHT // 10, 'path_img': './sprites/buttons/create_skin_button.png',
                'command': lambda: close_menu_run_generator(root)},
               {'x': WIDTH // 2, 'y': HEIGHT * 4 // 9 + HEIGHT // 5, 'path_img': './sprites/buttons/achievements_button.png',
                'command': lambda: open_achievement_window(root)},
               {'x': WIDTH // 2, 'y': HEIGHT * 4 // 9 + HEIGHT * 3 // 10, 'path_img': './sprites/buttons/reset_button.png',
                'command': lambda: set_player_default_file('./players/player.txt')}]

    window = Window(root, title='Treefinity Garden', size=[WIDTH, HEIGHT], path_icon='./sprites/icon.ico',
                    path_background_img='./sprites/backgrounds/window_background.png', buttons=buttons)

    icon = PhotoImage(file='./sprites/icon.png')
    window.canvas.create_image(135, 30, anchor='nw', image=icon)

    name_of_project = PhotoImage(file='./sprites/project_name.png')
    window.canvas.create_image(25, 210, anchor='nw', image=name_of_project)

    root.mainloop()