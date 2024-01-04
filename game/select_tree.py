import math
from tkinter import *
from tkinter import messagebox

from objects.window import Window
from objects.tree import Tree


def set_tree_canvases(gap_size, picture_tree_size, number_row, numbers_skins_on_last_row):
    canvases = []
    for y in range(number_row):
        if y == number_row - 1:
            max_column = numbers_skins_on_last_row
        else:
            max_column = 3
        for x in range(max_column):
            cur_canvas = {'name': 'tree' + str((x + 1) + 3 * y), 'bg': '#87cefa',
                          'coords': (gap_size + (gap_size + picture_tree_size) * x, gap_size + (gap_size + picture_tree_size) * y,
                                     (gap_size + picture_tree_size) * (x + 1), (gap_size + picture_tree_size) * (y + 1))}
            canvases.append(cur_canvas)

    return canvases


def draw_all_trees(window, player, picture_tree_size, lock_image):
    for i, (name, canvas) in enumerate(window.inner_canvases.items()):
        canvas.bind('<MouseWheel>', lambda event, cur_canvas=window.canvas: on_mouse_wheel(event, cur_canvas))
        tree = Tree(canvas, pos=(1 / 2, 60 / 63))
        tree.load_tree_from_json('tree' + str(i + 1))

        tree.trunk_length = 45
        tree.max_recursion_depth = 7
        tree.max_branch_thickness = 5
        tree.draw(warning_on=False)

        if str(i + 1) in player.skins and not player.skins[str(i + 1)][0]:
            tree.canvas.create_image(picture_tree_size // 3, picture_tree_size // 3, anchor='nw', image=lock_image)
            canvas.config(bg='#065b90')
        else:
            canvas.bind('<Button-1>', lambda event, cur_name=name, cur_player=player, root=window.root: choose_tree(cur_name, player, root))

        canvas.bind('<Enter>', lambda event, cur_canvas=canvas: draw_perimeter(cur_canvas))
        canvas.bind('<Leave>', lambda event, cur_canvas=canvas: delete_perimeter(cur_canvas))


def draw_perimeter(cur_canvas):
    width = 5
    cur_canvas.create_rectangle(4, 4, cur_canvas.winfo_reqwidth() - 4 - width, cur_canvas.winfo_reqheight() - 4 - width, width=width, tags='perimeter')


def delete_perimeter(cur_canvas):
    cur_perimeter = cur_canvas.find_withtag('perimeter')
    cur_canvas.delete(cur_perimeter)


def choose_tree(cur_name, cur_player, root):
    if cur_player.garden.get_first_free_position() == -1:
        messagebox.showwarning('Warning', 'Max amount of trees was reached')
        return

    cur_player.garden.add_tree_from_file(cur_name)
    root.destroy()


def on_mouse_wheel(event, canvas):
    canvas.yview_scroll(-1 * (event.delta // 120), 'units')


def update_scroll_region(canvas, scroll_area):
    canvas.update_idletasks()
    canvas.config(scrollregion=scroll_area)


def open_window_of_select_tree(root, player):
    select_tree_window = Toplevel(root)

    with open('./trees/skin_counter.txt', 'r') as file:
        number_of_skins = int(file.readline().strip())

    number_row = math.ceil(number_of_skins / 3)
    numbers_skins_on_last_row = number_of_skins % 3
    if numbers_skins_on_last_row == 0:
        numbers_skins_on_last_row = 3

    WIDTH = 600
    HEIGHT = 600

    window = Window(select_tree_window, title='Select Tree', size=[WIDTH, HEIGHT],
                    path_icon='./sprites/icon.ico', path_background_img='./sprites/backgrounds/scroll_background.png',
                    canvases=set_tree_canvases(gap_size=30, picture_tree_size=160, number_row=number_row, numbers_skins_on_last_row=numbers_skins_on_last_row))

    scrollbar = Scrollbar(select_tree_window, command=window.canvas.yview)
    scrollbar.pack(side=RIGHT, fill='y')
    window.canvas.configure(yscrollcommand=scrollbar.set)

    window.canvas.bind('<MouseWheel>', lambda event, canvas=window.canvas: on_mouse_wheel(event, canvas))
    work_area = (0, 0, WIDTH, (160 + 30) * number_row + 30)
    window.canvas.bind('<Configure>', lambda event, canvas=window.canvas, scroll_area=work_area: update_scroll_region(canvas, scroll_area))

    padlock_image = PhotoImage(file='./sprites/padlock.png')

    draw_all_trees(window=window, player=player, picture_tree_size=160, lock_image=padlock_image)

    select_tree_window.mainloop()