from tkinter import *
from tkinter import messagebox

from objects.window import Window
from objects.tree import Tree


def set_tree_canvases(gap_size, picture_tree_size):
    canvases = []

    for y in range(3):
        for x in range(3):
            cur_canvas = {'name': 'tree' + str((x + 1) + 3 * y), 'bg': 'white',
                          'coords': (
                          gap_size + (gap_size + picture_tree_size) * x, gap_size + (gap_size + picture_tree_size) * y,
                          (gap_size + picture_tree_size) * (x + 1), (gap_size + picture_tree_size) * (y + 1))}
            canvases.append(cur_canvas)

    return canvases


def draw_all_trees(window, garden):
    for i, (name, canvas) in enumerate(window.inner_canvases.items()):
        tree = Tree(canvas, pos=(1 / 2, 61 / 63))
        tree.load_tree_from_json('tree' + str(i + 1))
        tree.trunk_length = 45
        tree.max_recursion_depth = 7
        tree.max_branch_thickness = 5
        tree.draw()

        canvas.bind('<Button-1>', lambda event, cur_name=name, cur_garden=garden, root=window.root: choose_tree(cur_name, cur_garden, root))


def choose_tree(cur_name, cur_garden, root):
    cur_garden.add_tree_from_file(cur_name)
    root.destroy()


def open_window_of_select_tree(root, garden):
    if garden.get_first_free_position() == -1:
        messagebox.showinfo("Warning", "Max amount of trees was reached")
        return

    select_tree_window = Toplevel(root)
    select_tree_window.resizable(False, False)
    select_tree_window.iconbitmap('./sprites/icon.ico')

    WIDTH = 600
    HEIGHT = 600

    x_coordinate = (root.winfo_screenwidth() - WIDTH) // 2
    y_coordinate = (root.winfo_screenheight() - HEIGHT) // 2
    select_tree_window.geometry(f'{WIDTH}x{HEIGHT}+{x_coordinate}+{y_coordinate}')

    window = Window(select_tree_window, title='Select Tree', size=[WIDTH, HEIGHT],
                    path_background_img='./sprites/backgrounds/window_background.png',
                    canvases=set_tree_canvases(gap_size=30, picture_tree_size=160))

    draw_all_trees(window, garden)