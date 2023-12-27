from tkinter import *

from objects.tree import Tree
from objects.window import Window
from objects.garden import Garden
from objects.player import Player
from game.select_tree import open_window_of_select_tree


def close_game(root, player, call_ids):
    from menu.menu import run_menu

    player.save_player()

    for call_id in call_ids:
        root.after_cancel(call_id)
    call_ids.clear()

    root.destroy()
    run_menu()


def run_game(root=None):
    root = Tk()
    root.protocol('WM_DELETE_WINDOW', lambda: close_game(root, player, call_ids))

    WIDTH = 1280
    HEIGHT = 720

    buttons = [{'x': WIDTH / 6,     'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/buttons/regular_buttons/sun.png', 'path_img_under_cursor': './sprites/buttons/under_cursor_buttons/sun.png',
                'command': lambda: player.garden.action(Tree.increase_trunk_length)},
               {'x': WIDTH / 6 * 2, 'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/buttons/regular_buttons/fertilizer.png', 'path_img_under_cursor': './sprites/buttons/under_cursor_buttons/fertilizer.png',
                'command': lambda: player.garden.action(Tree.increase_max_recursion_depth)},
               {'x': WIDTH / 6 * 3, 'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/buttons/regular_buttons/water.png', 'path_img_under_cursor': './sprites/buttons/under_cursor_buttons/water.png',
                'command': lambda: player.garden.action(Tree.change_branch_angle)},
               {'x': WIDTH / 6 * 4, 'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/buttons/regular_buttons/plant.png', 'path_img_under_cursor': './sprites/buttons/under_cursor_buttons/plant.png',
                'command': lambda: open_window_of_select_tree(root, player)},
               {'x': WIDTH / 6 * 5, 'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/buttons/regular_buttons/delete.png', 'path_img_under_cursor': './sprites/buttons/under_cursor_buttons/delete.png',
                'command': lambda: player.garden.delete_tree()}]

    window = Window(root, title='Treefinity Garden', size=[WIDTH, HEIGHT], path_icon='./sprites/icon.ico',
                    path_background_img='./sprites/backgrounds/window_background.png', buttons=buttons,
                    canvases=[{'name': 'garden', 'coords': (WIDTH / 64, WIDTH / 64, WIDTH - WIDTH / 64, HEIGHT - HEIGHT / 8),
                               'bg': 'blue', 'bg_picture': './sprites/backgrounds/summer_background.png'}])

    garden = Garden(canvas=window.inner_canvases['garden'])

    player = Player(name='Player1', garden=garden)
    player.load_player()

    player.garden.draw()

    call_ids = []
    window.root.after(500, player.check_all_achievements, root, call_ids)

    window.root.mainloop()