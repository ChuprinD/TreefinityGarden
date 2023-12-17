from tkinter import *
from tkinter import messagebox

from objects.window import Window
from objects.tree import Tree


def set_tree_canvases(gap_size, picture_tree_size):
    canvases = []

    for y in range(3):
        for x in range(3):
            cur_canvas = {'name': 'tree' + str((x + 1) + 3 * y), 'bg': '#87cefa',
                          'coords': (gap_size + (gap_size + picture_tree_size) * x, gap_size + (gap_size + picture_tree_size) * y,
                                     (gap_size + picture_tree_size) * (x + 1), (gap_size + picture_tree_size) * (y + 1))}
            canvases.append(cur_canvas)

    return canvases


def draw_all_trees(window, player, picture_tree_size, lock_image):
    for i, (name, canvas) in enumerate(window.inner_canvases.items()):
        tree = Tree(canvas, pos=(1 / 2, 61 / 63))
        tree.load_tree_from_json('tree' + str(i + 1))

        tree.trunk_length = 45
        tree.max_recursion_depth = 7
        tree.max_branch_thickness = 5
        tree.draw()

        if player.skins[str(i + 1)][0]:
            canvas.bind('<Button-1>', lambda event, cur_name=name, cur_player=player, root=window.root: choose_tree(cur_name, player, root))
        else:
            tree.canvas.create_image(picture_tree_size // 3, picture_tree_size // 3, anchor='nw', image=lock_image)

def choose_tree(cur_name, cur_player, root):
    if cur_player.garden.get_first_free_position() == -1:
        messagebox.showwarning('Warning', 'Max amount of trees was reached')
        return

    cur_player.garden.add_tree_from_file(cur_name)
    root.destroy()


def open_window_of_select_tree(root, player):
    select_tree_window = Toplevel(root)
    select_tree_window.resizable(False, False)
    select_tree_window.iconbitmap('./sprites/icon.ico')

    WIDTH = 600
    HEIGHT = 600

    window = Window(select_tree_window, title='Select Tree', size=[WIDTH, HEIGHT],
                    path_background_img='./sprites/backgrounds/window_background.png',
                    canvases=set_tree_canvases(gap_size=30, picture_tree_size=160))

    padlock_image = PhotoImage(file='./sprites/padlock.png')

    draw_all_trees(window=window, player=player, picture_tree_size=160, lock_image=padlock_image)

    window.canvas.pack()
    select_tree_window.mainloop()