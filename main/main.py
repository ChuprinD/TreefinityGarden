from tkinter import *
from objects.tree import Tree
from objects.window import Window
from objects.garden import Garden
from utilities.color import natural_coloring


def start_game():
    root = Tk()

    WIDTH = 1920
    HEIGHT = 1080

    buttons = [{'text': 'Add Water', 'x': 1380, 'y': 30, 'width': 510, 'height': 60,
                'command': lambda: garden.action(Tree.increase_trunk_length)},
               {'text': 'Add Sunlight', 'x': 1380, 'y': 120, 'width': 510, 'height': 60,
                'command': lambda: garden.action(Tree.increase_max_recursion_depth)},
               {'text': 'Add Fertlizer', 'x': 1380, 'y': 210, 'width': 510, 'height': 60,
                'command': lambda: garden.action(Tree.change_branch_angle)}]

    window = Window(root, title='Treefinity Garden', size=[WIDTH, HEIGHT],
                    path_background_img='./sprites/window_background.png', buttons=buttons,
                    canvases=[{'name': 'garden', 'coords': (30, 30, 1350, 1050), 'bg': 'blue', 'bg_picture': './sprites/garden_background.png'}])

    garden = Garden(canvas=window.inner_canvases['garden'])

    tree = Tree(canvas=window.inner_canvases['garden'], pos=(window.inner_canvases['garden'].winfo_reqwidth() / 2, window.inner_canvases['garden'].winfo_reqheight() - 30),
                trunk_length=200, trunk_angle=90, branch_angle=[30, 60], branch_length_coefficient=0.7, max_recursion_depth=7, min_branch_thickness=1,
                max_branch_thickness=4, color_function=natural_coloring)

    garden.add_tree(tree)
    garden.draw()

    window.canvas.pack()
    root.mainloop()
