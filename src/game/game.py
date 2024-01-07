from tkinter import *

from src.objects.tree import Tree
from src.objects.window import Window
from src.objects.garden import Garden
from src.objects.player import Player
from src.game.select_tree import open_window_of_select_tree


def close_game(root, player, call_ids):
    from src.menu.menu import run_menu

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

    buttons = [{'name': 'magnifier',  'x': WIDTH / 7,     'y': HEIGHT - HEIGHT / 16 - 3,
                'path_img': 'resources/sprites/buttons/regular_buttons/magnifier_off.png', 'path_img_under_cursor': 'resources/sprites/buttons/under_cursor_buttons/magnifier_off.png',
                'command': lambda: player.garden.zoom.activate_zoom(window)},
               {'name': 'sun',        'x': WIDTH / 7 * 2, 'y': HEIGHT - HEIGHT / 16 - 3,
                'path_img': 'resources/sprites/buttons/regular_buttons/sun.png', 'path_img_under_cursor': 'resources/sprites/buttons/under_cursor_buttons/sun.png',
                'command': lambda: player.garden.action(Tree.increase_trunk_length)},
               {'name': 'fertilizer', 'x': WIDTH / 7 * 3, 'y': HEIGHT - HEIGHT / 16 - 3,
                'path_img': 'resources/sprites/buttons/regular_buttons/fertilizer.png', 'path_img_under_cursor': 'resources/sprites/buttons/under_cursor_buttons/fertilizer.png',
                'command': lambda: player.garden.action(Tree.increase_max_recursion_depth)},
               {'name': 'water',      'x': WIDTH / 7 * 4, 'y': HEIGHT - HEIGHT / 16 - 3,
                'path_img': 'resources/sprites/buttons/regular_buttons/water.png', 'path_img_under_cursor': 'resources/sprites/buttons/under_cursor_buttons/water.png',
                'command': lambda: player.garden.action(Tree.change_branch_angle)},
               {'name': 'plant',      'x': WIDTH / 7 * 5, 'y': HEIGHT - HEIGHT / 16 - 3,
                'path_img': 'resources/sprites/buttons/regular_buttons/plant.png', 'path_img_under_cursor': 'resources/sprites/buttons/under_cursor_buttons/plant.png',
                'command': lambda: open_window_of_select_tree(root, player)},
               {'name': 'delete',     'x': WIDTH / 7 * 6, 'y': HEIGHT - HEIGHT / 16 - 3,
                'path_img': 'resources/sprites/buttons/regular_buttons/delete.png', 'path_img_under_cursor': 'resources/sprites/buttons/under_cursor_buttons/delete.png',
                'command': lambda: player.garden.delete_tree()}]

    window = Window(root, title='Treefinity Garden', size=[WIDTH, HEIGHT], path_icon='resources/sprites/icon.ico',
                    path_background_img='resources/sprites/backgrounds/window_background.png', buttons=buttons,
                    canvases=[{'name': 'garden', 'coords': (WIDTH / 64, WIDTH / 64, WIDTH - WIDTH / 64, HEIGHT - HEIGHT / 8),
                               'bg': 'blue', 'bg_picture': 'resources/sprites/backgrounds/summer_background.png'}])

    garden = Garden(canvas=window.inner_canvases['garden'])

    player = Player(name='Player1', garden=garden)
    player.load_player()

    player.garden.draw(warning_on=True)

    call_ids = []
    window.root.after(500, player.check_all_achievements, root, call_ids)

    window.root.mainloop()