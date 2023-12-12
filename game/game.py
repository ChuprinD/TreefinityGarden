from tkinter import *

from objects.tree import Tree
from objects.window import Window
from objects.garden import Garden


def close_game(root):
    from menu.menu import run_menu

    root.destroy()
    run_menu()


def run_game():
    root = Tk()
    root.iconbitmap('./sprites/icon.ico')
    root.protocol("WM_DELETE_WINDOW", lambda: close_game(root))

    WIDTH = 1280
    HEIGHT = 720

    root.geometry(str(WIDTH) + 'x' + str(HEIGHT))

    buttons = [{'x': WIDTH / 5, 'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/buttons/sun_button.png',
                'command': lambda: garden.action(Tree.increase_trunk_length)},
               {'x': WIDTH / 5 * 2, 'y': HEIGHT - HEIGHT / 16 - 3,
                'path_img': './sprites/buttons/fertilizer_button.png',
                'command': lambda: garden.action(Tree.increase_max_recursion_depth)},
               {'x': WIDTH / 5 * 3, 'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/buttons/water_button.png',
                'command': lambda: garden.action(Tree.change_branch_angle)},
               {'x': WIDTH / 5 * 4, 'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/buttons/plant_button.png',
                'command': lambda: garden.add_random_tree()}]

    window = Window(root, title='Treefinity Garden', size=[WIDTH, HEIGHT],
                    path_background_img='./sprites/backgrounds/window_background.png', buttons=buttons,
                    canvases=[
                        {'name': 'garden', 'coords': (WIDTH / 64, WIDTH / 64, WIDTH - WIDTH / 64, HEIGHT - HEIGHT / 8),
                         'bg': 'blue', 'bg_picture': './sprites/backgrounds/summer_background.png'}])

    garden = Garden(canvas=window.inner_canvases['garden'])

    tree = Tree(canvas=window.inner_canvases['garden'], pos=(0, 0),
                trunk_length=100, trunk_angle=90, branch_angle=(30, 60), branch_length_coefficient=0.7,
                max_recursion_depth=2, min_branch_thickness=1,
                max_branch_thickness=4, color_function_name='default_coloring')

    garden.set_tree_on_position(tree, 2)
    garden.draw()

    window.canvas.pack()
    root.mainloop()
