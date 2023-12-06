from tkinter import *
import tkinter.ttk as ttk
from objects.tree import Tree
from objects.window import Window
from objects.garden import Garden
from utilities.color import COLORINGS
from utilities.json import set_data_to_file


def create_slider(parent, update_callback, minimum, maximum, pos, initial_value, label_text, ratio=1) -> Scale:
    label = Label(parent, text=label_text)
    label.place(x=pos[0] - label.winfo_reqwidth(), y=pos[1])

    slider = Scale(parent, from_=minimum, to=maximum, orient="horizontal", command=update_callback,
                   variable=DoubleVar(value=initial_value), resolution=ratio, length=WIDTH * 5 / 32)

    slider.place(x=pos[0], y=pos[1])
    return slider


def update_trunk_length(value):
    tree.trunk_length = int(value)
    garden.draw()


def update_branch_length_coefficient(value):
    tree.branch_length_coefficient = float(value)
    garden.draw()


def update_max_recursion_depth(value):
    tree.max_recursion_depth = int(value)
    garden.draw()


def update_branch_angle1(value):
    tree.branch_angle = (int(value), tree.branch_angle[1])
    garden.draw()


def update_branch_angle2(value):
    tree.branch_angle = (tree.branch_angle[0], int(value))
    garden.draw()


def update_max_branch_thickness(value):
    tree.max_branch_thickness = int(value)
    garden.draw()


def update_color_function_name(event):
    tree.color_function_name = str(combobox_color.get())
    garden.draw()


def create_file(window, name):
    cur_tree = {'trunk_length': tree.trunk_length, 'branch_length_coefficient': tree.branch_length_coefficient,
                'max_recursion_depth': tree.max_recursion_depth, 'branch_angle': tree.branch_angle,
                'max_branch_thickness': tree.max_branch_thickness, 'color_function_name': tree.color_function_name}

    set_data_to_file(cur_tree, '../trees/' + name + '.txt')
    close_window(window)


def load_file(window, name):
    tree.load_tree_from_json(name)

    slider_trunk_length.set(tree.trunk_length)
    slider_branch_length_coefficient.set(tree.branch_length_coefficient)
    slider_max_recursion_depth.set(tree.max_recursion_depth)
    slider_branch_angle1.set(tree.branch_angle[0])
    slider_branch_angle2.set(tree.branch_angle[1])
    slider_max_branch_thickness.set(tree.max_branch_thickness)

    close_window(window)


def close_window(window):
    window.destroy()


def enter_tree_name(root):
    enter_window = Toplevel(root)
    enter_window.title('Save tree')
    enter_window.geometry(f'{WIDTH // 3}x{HEIGHT // 3}+{WIDTH // 3}+{HEIGHT // 3}')

    entry = Entry(enter_window, font=("Arial", 12))
    entry.place(x=WIDTH / 18, y=HEIGHT / 9, width=WIDTH * 2 / 9, height=HEIGHT / 25)

    button_create = Button(enter_window, text="Save tree", command=lambda: create_file(enter_window, entry.get()))
    button_create.place(x=WIDTH / 9, y=HEIGHT * 2 / 9, width=WIDTH / 9, height=HEIGHT / 22)

    button_close = Button(enter_window, text="Close", command=lambda: close_window(enter_window))
    button_close.place(x=WIDTH / 9, y=HEIGHT * 2 / 9 + HEIGHT / 22 + 10, width=WIDTH / 9, height=HEIGHT / 22)


def load_tree(root):
    enter_window = Toplevel(root)
    enter_window.title('Load tree')
    enter_window.geometry(f'{WIDTH // 3}x{HEIGHT // 3}+{WIDTH // 3}+{HEIGHT // 3}')

    entry = Entry(enter_window, font=("Arial", 12))
    entry.place(x=WIDTH / 18, y=HEIGHT / 9, width=WIDTH * 2 / 9, height=HEIGHT / 25)

    button_create = Button(enter_window, text="Load tree", command=lambda: load_file(enter_window, entry.get()))
    button_create.place(x=WIDTH / 9, y=HEIGHT * 2 / 9, width=WIDTH / 9, height=HEIGHT / 22)


root = Tk()
root.title('DEV APP')
WIDTH = 1280
HEIGHT = 720

window = Window(root, title='Treefinity Garden', size=[WIDTH, HEIGHT],
                path_background_img='../sprites/window_background.png',
                canvases=[{'name': 'garden',
                           'coords': (WIDTH / 64, HEIGHT / 64, WIDTH / 64 + WIDTH * 2 / 3, HEIGHT - HEIGHT / 64),
                           'bg': 'blue',
                           'bg_picture': '../sprites/garden_background.png'}])

garden = Garden(canvas=window.inner_canvases['garden'])

tree = Tree(canvas=window.inner_canvases['garden'],
            pos=(window.inner_canvases['garden'].winfo_reqwidth() / 2,
                 window.inner_canvases['garden'].winfo_reqheight() - HEIGHT / 64),
            trunk_length=150, trunk_angle=90, branch_angle=(30, 60), branch_length_coefficient=0.7,
            max_recursion_depth=7, min_branch_thickness=1,
            max_branch_thickness=4, color_function_name='natural_coloring')

slider_pos_x = WIDTH / 64 * 2 + WIDTH * 2 / 3 + WIDTH * 55 / 384 - WIDTH * 3 / 64

slider_trunk_length = create_slider(parent=window.canvas, minimum=0, maximum=400,
                                    update_callback=update_trunk_length, pos=(slider_pos_x, HEIGHT / 64),
                                    label_text='trunk_length', initial_value=tree.trunk_length)

slider_branch_length_coefficient = create_slider(parent=window.canvas, minimum=0, maximum=1,
                                                 update_callback=update_branch_length_coefficient,
                                                 pos=(slider_pos_x, HEIGHT / 64 + 60),
                                                 ratio=0.005, label_text='branch_length_coefficient',
                                                 initial_value=tree.branch_length_coefficient)

slider_max_recursion_depth = create_slider(parent=window.canvas, minimum=2, maximum=15,
                                           update_callback=update_max_recursion_depth,
                                           pos=(slider_pos_x, HEIGHT / 64 + 120),
                                           label_text='max_recursion_depth', initial_value=tree.max_recursion_depth)

slider_branch_angle1 = create_slider(parent=window.canvas, minimum=-90, maximum=90,
                                     update_callback=update_branch_angle1, pos=(slider_pos_x, HEIGHT / 64 + 180),
                                     label_text='max_trunk_angle1', initial_value=tree.branch_angle[0])

slider_branch_angle2 = create_slider(parent=window.canvas, minimum=-90, maximum=90,
                                     update_callback=update_branch_angle2, pos=(slider_pos_x, HEIGHT / 64 + 240),
                                     label_text='max_trunk_angle1', initial_value=tree.branch_angle[1])

slider_max_branch_thickness = create_slider(parent=window.canvas, minimum=1, maximum=20,
                                            update_callback=update_max_branch_thickness,
                                            pos=(slider_pos_x, HEIGHT / 64 + 300),
                                            label_text='max_trunk_angle1', initial_value=tree.max_branch_thickness)

combobox_color = ttk.Combobox(window.canvas, values=list(COLORINGS.keys()))
combobox_color.set(tree.color_function_name)
combobox_color.place(x=slider_pos_x, y=HEIGHT / 64 + 360)
combobox_color.bind("<<ComboboxSelected>>", update_color_function_name)
label_combobox_color = Label(window.canvas, text='combobox_color')
label_combobox_color.place(x=slider_pos_x - label_combobox_color.winfo_reqwidth(), y=HEIGHT / 64 + 360)

save_button = Button(window.canvas, text='save tree', command=lambda: enter_tree_name(root))
save_button.place(x=WIDTH - WIDTH / 64 - WIDTH * 13 / 64, y=HEIGHT - HEIGHT / 64 - HEIGHT / 17, width=WIDTH * 5 / 32,
                  height=HEIGHT / 17)

load_button = Button(window.canvas, text='load tree', command=lambda: load_tree(root))
load_button.place(x=WIDTH - WIDTH / 64 - WIDTH * 13 / 64, y=HEIGHT - HEIGHT * 2 / 64 - HEIGHT * 2 / 17,
                  width=WIDTH * 5 / 32, height=HEIGHT / 17)

garden.add_tree(tree)
garden.draw()

window.canvas.pack()
root.mainloop()
