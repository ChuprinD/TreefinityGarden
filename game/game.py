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
    root.iconbitmap('./sprites/icon.ico')
    root.protocol("WM_DELETE_WINDOW", lambda: close_game(root, player, call_ids))

    WIDTH = 1280
    HEIGHT = 720
    x_coordinate = (root.winfo_screenwidth() - WIDTH) // 2
    y_coordinate = (root.winfo_screenheight() - HEIGHT) // 2

    root.geometry(f'{WIDTH}x{HEIGHT}+{x_coordinate}+{y_coordinate}')

    buttons = [{'x': WIDTH / 6, 'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/buttons/sun_button.png',
                'command': lambda: player.garden.action(Tree.increase_trunk_length)},
               {'x': WIDTH / 6 * 2, 'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/buttons/fertilizer_button.png',
                'command': lambda: player.garden.action(Tree.increase_max_recursion_depth)},
               {'x': WIDTH / 6 * 3, 'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/buttons/water_button.png',
                'command': lambda: player.garden.action(Tree.change_branch_angle)},
               {'x': WIDTH / 6 * 4, 'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/buttons/plant_button.png',
                'command': lambda: open_window_of_select_tree(root, player)},
               {'x': WIDTH / 6 * 5, 'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/buttons/delete_button.png',
                'command': lambda: player.garden.delete_tree()}]

    window = Window(root, title='Treefinity Garden', size=[WIDTH, HEIGHT],
                    path_background_img='./sprites/backgrounds/window_background.png', buttons=buttons,
                    canvases=[{'name': 'garden', 'coords': (WIDTH / 64, WIDTH / 64, WIDTH - WIDTH / 64, HEIGHT - HEIGHT / 8),
                               'bg': 'blue', 'bg_picture': './sprites/backgrounds/summer_background.png'}])

    garden = Garden(canvas=window.inner_canvases['garden'])

    player = Player(name='Player1', garden=garden)
    player.load_player()

    player.garden.draw()

    window.canvas.pack()

    call_ids = []
    root.after(500, player.check_all_achievements, root, call_ids)

    root.mainloop()