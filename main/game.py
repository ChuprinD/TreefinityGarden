from tkinter import *
from objects.tree import Tree
from objects.window import Window


def start_game():
    root = Tk()

    WIDTH = 1920
    HEIGHT = 1080

    cur_tree = None

    buttons = [{'text': 'Add Water', 'x': 1380, 'y': 30, 'width': 510, 'height': 60,
                'command': lambda: Tree.increase_trunk_length(cur_tree)},
               {'text': 'Add Sunlight', 'x': 1380, 'y': 120, 'width': 510, 'height': 60,
                'command': lambda: Tree.increase_max_recursion_depth(cur_tree)},
               {'text': 'Add Fertlizer', 'x': 1380, 'y': 210, 'width': 510, 'height': 60,
                'command': lambda: Tree.change_branch_angle(cur_tree)}]

    window = Window(root, title="Treefinity Garden", size=[WIDTH, HEIGHT],
                    path_background_img="./sprites/background.png", buttons=buttons,
                    rectangles=[(30, 30, 1350, 1050)])

    window.inner_canvases[0].config(bg="blue")

    tree = Tree(canvas=window.inner_canvases[0], pos=[window.inner_canvases[0].winfo_width() / 2, window.inner_canvases[0].winfo_height() - 30],
                trunk_length=200, trunk_angle=90, branch_angle=[30, 60], branch_length_coefficient=0.7, max_recursion_depth=7, min_branch_thickness=1,
                max_branch_thickness=4)
    cur_tree = tree

    tree.draw()
    window.canvas.pack()
    root.mainloop()
