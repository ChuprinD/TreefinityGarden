from tkinter import *

from objects.tree import Tree
from objects.window import Window
from objects.garden import Garden


def start_game():
    root = Tk()
    root.resizable(False, False)

    WIDTH = 1280
    HEIGHT = 720

    root.geometry(str(WIDTH) + 'x' + str(HEIGHT))

    buttons = [{'x': WIDTH / 5, 'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/sun_button.png',
                'command': lambda: garden.action(Tree.increase_trunk_length)},
               {'x': WIDTH / 5 * 2, 'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/fertilizer_button.png',
                'command': lambda: garden.action(Tree.increase_max_recursion_depth)},
               {'x': WIDTH / 5 * 3, 'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/water_button.png',
                'command': lambda: garden.action(Tree.change_branch_angle)},
               {'x': WIDTH / 5 * 4, 'y': HEIGHT - HEIGHT / 16 - 3, 'path_img': './sprites/plant_button.png',
                'command': lambda: garden.add_random_tree()}]

    window = Window(root, title='Treefinity Garden', size=[WIDTH, HEIGHT],
                    path_background_img='./sprites/window_background.png', buttons=buttons,
                    canvases=[
                        {'name': 'garden', 'coords': (WIDTH / 64, WIDTH / 64, WIDTH - WIDTH / 64, HEIGHT - HEIGHT / 8),
                         'bg': 'blue', 'bg_picture': './sprites/garden_background.png'}])

    garden = Garden(canvas=window.inner_canvases['garden'])

    tree = Tree(canvas=window.inner_canvases['garden'], pos=(0, 0),
                trunk_length=100, trunk_angle=90, branch_angle=(30, 60), branch_length_coefficient=0.7,
                max_recursion_depth=6, min_branch_thickness=1,
                max_branch_thickness=4, color_function_name='default_coloring')

    garden.set_tree_on_position(tree, 2)
    garden.draw()

    window.canvas.pack()
    root.mainloop()
