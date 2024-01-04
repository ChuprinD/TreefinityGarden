from tkinter import *
import tkinter.ttk as ttk
from tkinter import messagebox

from objects.tree import Tree
from objects.window import Window
from objects.garden import Garden
from utilities.color import COLORINGS
from utilities.json import set_tree_to_file


def close_generator(root):
    from menu.menu import run_menu
    root.destroy()
    run_menu()


def create_slider(parent, update_callback, minimum, maximum, pos, initial_value, label_text, ratio=1):
    label = Label(parent, text=label_text)
    label.place(x=pos[0], y=pos[1] + 40)

    slider = Scale(parent, from_=minimum, to=maximum, orient='horizontal', command=lambda value: update_callback(value, slider.set),
                   variable=DoubleVar(value=initial_value), resolution=ratio, length=200)

    slider.place(x=pos[0], y=pos[1])
    return slider


def update_trunk_length(value, callback):
    global garden
    old_trunk_length = garden.trees[garden.index_cur_tree].trunk_length
    garden.trees[garden.index_cur_tree].trunk_length = int(value)

    if not garden.trees[garden.index_cur_tree].check_tree_visibility(warning_on=False):
        garden.trees[garden.index_cur_tree].trunk_length = old_trunk_length
        callback(old_trunk_length)

    garden.draw(warning_on=False)


def update_branch_length_coefficient(value, callback):
    global garden
    old_branch_length_coefficient = garden.trees[garden.index_cur_tree].branch_length_coefficient
    garden.trees[garden.index_cur_tree].branch_length_coefficient = float(value)

    if not garden.trees[garden.index_cur_tree].check_tree_visibility(warning_on=False):
        garden.trees[garden.index_cur_tree].branch_length_coefficient = old_branch_length_coefficient
        callback(old_branch_length_coefficient)

    garden.draw(warning_on=False)


def update_max_recursion_depth(value, callback):
    global garden
    old_max_recursion_depth = garden.trees[garden.index_cur_tree].max_recursion_depth
    garden.trees[garden.index_cur_tree].max_recursion_depth = int(value)

    if not garden.trees[garden.index_cur_tree].check_tree_visibility(warning_on=False):
        garden.trees[garden.index_cur_tree].max_recursion_depth = old_max_recursion_depth
        callback(old_max_recursion_depth)

    garden.draw(warning_on=False)


def update_branch_angle1(value, callback):
    global garden
    old_branch_angle1 = garden.trees[garden.index_cur_tree].branch_angle[0]
    garden.trees[garden.index_cur_tree].branch_angle = (int(value), garden.trees[garden.index_cur_tree].branch_angle[1])

    if not garden.trees[garden.index_cur_tree].check_tree_visibility(warning_on=False):
        garden.trees[garden.index_cur_tree].branch_angle = (old_branch_angle1, garden.trees[garden.index_cur_tree].branch_angle[1])
        callback(old_branch_angle1)

    garden.draw(warning_on=False)


def update_branch_angle2(value, callback):
    global garden
    old_branch_angle2 = garden.trees[garden.index_cur_tree].branch_angle[1]
    garden.trees[garden.index_cur_tree].branch_angle = (garden.trees[garden.index_cur_tree].branch_angle[0], int(value))

    if not garden.trees[garden.index_cur_tree].check_tree_visibility(warning_on=False):
        garden.trees[garden.index_cur_tree].branch_angle = (garden.trees[garden.index_cur_tree].branch_angle[0], old_branch_angle2)
        callback(old_branch_angle2)

    garden.draw(warning_on=False)


def update_max_branch_thickness(value, callback):
    global garden
    old_max_branch_thickness = garden.trees[garden.index_cur_tree].max_branch_thickness
    garden.trees[garden.index_cur_tree].max_branch_thickness = int(value)

    if not garden.trees[garden.index_cur_tree].check_tree_visibility(warning_on=False):
        garden.trees[garden.index_cur_tree].max_branch_thickness = old_max_branch_thickness
        callback(old_max_branch_thickness)

    garden.draw(warning_on=False)


def update_color_function_name(pos):
    global garden
    garden.trees[garden.index_cur_tree].color_function_name = str(pos)
    garden.draw(warning_on=False)


def create_file(window=None, name='test'):
    cur_tree = {'branch_length_coefficient': garden.trees[garden.index_cur_tree].branch_length_coefficient, 'branch_angle': garden.trees[garden.index_cur_tree].branch_angle,
                'max_branch_thickness': garden.trees[garden.index_cur_tree].max_branch_thickness, 'color_function_name': garden.trees[garden.index_cur_tree].color_function_name}

    set_tree_to_file(cur_tree, './trees/' + name + '.txt')
    messagebox.showinfo('Saved', 'You have successfully saved the skin!')

    if window is not None:
        window.destroy()


def load_file(window, name):
    global garden
    garden.trees[garden.index_cur_tree].load_tree_from_json(name)
    garden.draw(warning_on=False)

    window.destroy()


def enter_tree_name(root):
    global SIZE, is_it_admin

    if is_it_admin:
        enter_window = Toplevel(root)
        enter_window.resizable(False, False)
        enter_window.title('Save tree')
        enter_window.iconbitmap('./sprites/icon.ico')

        x_coordinate = (root.winfo_screenwidth() - SIZE[0] // 3) // 2
        y_coordinate = (root.winfo_screenheight() - SIZE[1] // 3) // 2
        enter_window.geometry(f'{SIZE[0] // 3}x{SIZE[1] // 3}+{x_coordinate}+{y_coordinate}')

        entry = Entry(enter_window, font=('Arial', 12))
        entry.place(x=SIZE[0] / 18, y=SIZE[1] / 9, width=SIZE[0] * 2 / 9, height=SIZE[1] / 25)

        button_create = Button(enter_window, text='Save tree', command=lambda: create_file(enter_window, entry.get()))
        button_create.place(x=SIZE[0] / 9, y=SIZE[1] * 2 / 9, width=SIZE[0] / 9, height=SIZE[1] / 22)
        enter_window.mainloop()
    else:
        if messagebox.askokcancel('Confirmation', 'Are you sure you want to save this tree?'):
            with open('./trees/skin_counter.txt', 'r') as file:
                number = int(file.readline().strip())

            number += 1

            create_file(name='tree' + str(number))

            with open('./trees/skin_counter.txt', 'w') as file:
                file.write(str(number))


def load_tree(root):
    global SIZE
    enter_window = Toplevel(root)
    enter_window.resizable(False, False)
    enter_window.title('Load tree')
    enter_window.iconbitmap('./sprites/icon.ico')

    x_coordinate = (root.winfo_screenwidth() - SIZE[0] // 3) // 2
    y_coordinate = (root.winfo_screenheight() - SIZE[1] // 3) // 2
    enter_window.geometry(f'{SIZE[0] // 3}x{SIZE[1] // 3}+{x_coordinate}+{y_coordinate}')

    entry = Entry(enter_window, font=('Arial', 12))
    entry.place(x=SIZE[0] / 18, y=SIZE[1] / 9, width=SIZE[0] * 2 / 9, height=SIZE[1] / 25)

    button_create = Button(enter_window, text='Load tree', command=lambda: load_file(enter_window, entry.get()))
    button_create.place(x=SIZE[0] / 9, y=SIZE[1] * 2 / 9, width=SIZE[0] / 9, height=SIZE[1] / 22)


def change_tree_position(pos):
    global garden
    position = int(pos)
    garden.trees[garden.index_cur_tree].pos = garden.trees_pos[position]
    garden.trees[garden.index_cur_tree], garden.trees[pos] = garden.trees[pos], garden.trees[garden.index_cur_tree]
    garden.index_cur_tree = pos
    garden.draw(warning_on=False)


def change_season(season):
    global garden
    garden.cur_season = season
    garden.draw(warning_on=False)


def open_tool_window(root):
    global garden, SIZE
    tool_window = Toplevel(root)
    tool_window.resizable(False, False)
    tool_window.title('Tool Window')
    tool_window.iconbitmap('./sprites/icon.ico')

    x_coordinate = (root.winfo_screenwidth() - SIZE[0] // 2) // 2
    y_coordinate = (root.winfo_screenheight() - SIZE[1] // 2) // 2
    tool_window.geometry(f'{SIZE[0] // 3 + 30}x{SIZE[1] // 2}+{x_coordinate}+{y_coordinate}')

    slider_pos = (10, 0)
    slider_trunk_length = create_slider(parent=tool_window, minimum=0, maximum=300,
                                        update_callback=update_trunk_length, pos=(slider_pos[0], slider_pos[1]),
                                        label_text='trunk_length', initial_value=garden.trees[garden.index_cur_tree].trunk_length)

    slider_branch_length_coefficient = create_slider(parent=tool_window, minimum=0, maximum=0.7,
                                                     update_callback=update_branch_length_coefficient,
                                                     pos=(slider_pos[0], slider_pos[1] + 60),
                                                     ratio=0.005, label_text='branch_length_coefficient',
                                                     initial_value=garden.trees[garden.index_cur_tree].branch_length_coefficient)

    slider_max_recursion_depth = create_slider(parent=tool_window, minimum=2, maximum=15,
                                               update_callback=update_max_recursion_depth,
                                               pos=(slider_pos[0], slider_pos[1] + 120),
                                               label_text='max_recursion_depth', initial_value=garden.trees[garden.index_cur_tree].max_recursion_depth)

    slider_branch_angle1 = create_slider(parent=tool_window, minimum=-90, maximum=90,
                                         update_callback=update_branch_angle1, pos=(slider_pos[0], slider_pos[1] + 180),
                                         label_text='max_trunk_angle1', initial_value=garden.trees[garden.index_cur_tree].branch_angle[0])

    slider_branch_angle2 = create_slider(parent=tool_window, minimum=-90, maximum=90,
                                         update_callback=update_branch_angle2, pos=(slider_pos[0], slider_pos[1] + 240),
                                         label_text='max_trunk_angle1', initial_value=garden.trees[garden.index_cur_tree].branch_angle[1])

    slider_max_branch_thickness = create_slider(parent=tool_window, minimum=1, maximum=20,
                                                update_callback=update_max_branch_thickness,
                                                pos=(slider_pos[0], slider_pos[1] + 300),
                                                label_text='max_trunk_angle1', initial_value=garden.trees[garden.index_cur_tree].max_branch_thickness)

    combobox_color_pos = (250, 25)
    combobox_color = ttk.Combobox(tool_window, values=list(COLORINGS.keys()))
    combobox_color.set(garden.trees[garden.index_cur_tree].color_function_name)
    combobox_color.place(x=combobox_color_pos[0], y=combobox_color_pos[1])
    combobox_color.bind('<<ComboboxSelected>>', lambda event: update_color_function_name(combobox_color.get()))
    label_combobox_color = Label(tool_window, text='combobox_color')
    label_combobox_color.place(x=combobox_color_pos[0], y=combobox_color_pos[1] - 25)

    cur_tree_pos = IntVar()
    radiobutton_tree_pos = (250, 60)
    r_position_0 = Radiobutton(tool_window, text='Position 0', variable=cur_tree_pos, value=0,
                               command=lambda: change_tree_position(cur_tree_pos.get()))
    r_position_0.place(x=radiobutton_tree_pos[0], y=radiobutton_tree_pos[1])

    r_position_1 = Radiobutton(tool_window, text='Position 1', variable=cur_tree_pos, value=1,
                               command=lambda: change_tree_position(cur_tree_pos.get()))
    r_position_1.place(x=radiobutton_tree_pos[0], y=radiobutton_tree_pos[1] + 30)

    r_position_2 = Radiobutton(tool_window, text='Position 2', variable=cur_tree_pos, value=2,
                               command=lambda: change_tree_position(cur_tree_pos.get()))
    r_position_2.place(x=radiobutton_tree_pos[0], y=radiobutton_tree_pos[1] + 60)

    r_position_3 = Radiobutton(tool_window, text='Position 3', variable=cur_tree_pos, value=3,
                               command=lambda: change_tree_position(cur_tree_pos.get()))
    r_position_3.place(x=radiobutton_tree_pos[0], y=radiobutton_tree_pos[1] + 90)

    r_position_4 = Radiobutton(tool_window, text='Position 4', variable=cur_tree_pos, value=4,
                               command=lambda: change_tree_position(cur_tree_pos.get()))
    r_position_4.place(x=radiobutton_tree_pos[0], y=radiobutton_tree_pos[1] + 120)

    match garden.index_cur_tree:
        case 0:
            r_position_0.select()
        case 1:
            r_position_1.select()
        case 2:
            r_position_2.select()
        case 3:
            r_position_3.select()
        case 4:
            r_position_4.select()

    cur_season = IntVar()
    radiobutton_season = (350, 60)
    r_summer = Radiobutton(tool_window, text='Summer', variable=cur_season, value=0,
                           command=lambda: change_season(cur_season.get()))
    r_summer.place(x=radiobutton_season[0], y=radiobutton_season[1])

    r_autumn = Radiobutton(tool_window, text='Autumn', variable=cur_season, value=1,
                           command=lambda: change_season(cur_season.get()))
    r_autumn.place(x=radiobutton_season[0], y=radiobutton_season[1] + 30)

    r_winter = Radiobutton(tool_window, text='Winter', variable=cur_season, value=2,
                           command=lambda: change_season(cur_season.get()))
    r_winter.place(x=radiobutton_season[0], y=radiobutton_season[1] + 60)

    r_spring = Radiobutton(tool_window, text='Spring', variable=cur_season, value=3,
                           command=lambda: change_season(cur_season.get()))
    r_spring.place(x=radiobutton_season[0], y=radiobutton_season[1] + 90)

    match garden.cur_season:
        case 0:
            r_summer.select()
        case 1:
            r_autumn.select()
        case 2:
            r_winter.select()
        case 3:
            r_spring.select()


def run_generator(admin):
    global window, garden, SIZE, is_it_admin
    is_it_admin = admin
    root = Tk()

    root.protocol('WM_DELETE_WINDOW', lambda: close_generator(root))

    buttons = [{'name': 'save', 'x': SIZE[0] // 4, 'y': SIZE[1] * 14 // 15, 'path_img': './sprites/buttons/regular_buttons/save.png',
                'path_img_under_cursor': './sprites/buttons/under_cursor_buttons/save.png',
                'command': lambda: enter_tree_name(root)},
               {'name': 'tool_window', 'x': SIZE[0] * 3 // 4, 'y': SIZE[1] * 14 // 15,
                'path_img': './sprites/buttons/regular_buttons/tool_window.png',
                'path_img_under_cursor': './sprites/buttons/under_cursor_buttons/tool_window.png',
                'command': lambda: open_tool_window(root)}]

    if is_it_admin:
        buttons.append({'name': 'load_tree', 'x': SIZE[0] * 2 // 4, 'y': SIZE[1] * 14 // 15, 'path_img': './sprites/buttons/regular_buttons/load_tree.png',
                        'path_img_under_cursor': './sprites/buttons/under_cursor_buttons/load_tree.png',
                        'command': lambda: load_tree(root)})

    window = Window(root, title='Skin Creator', size=[SIZE[0], SIZE[1]], path_icon='./sprites/icon.ico',
                    path_background_img='./sprites/backgrounds/window_background.png', buttons=buttons,
                    canvases=[{'name': 'garden', 'bg': 'blue', 'bg_picture': './sprites/backgrounds/summer_background.png',
                               'coords': (SIZE[0] / 64, SIZE[0] / 64, SIZE[0] - SIZE[0] / 64, SIZE[1] - SIZE[1] / 8)}])

    garden = Garden(canvas=window.inner_canvases['garden'])

    tree = Tree(canvas=window.inner_canvases['garden'], pos=(0, 0), trunk_length=100,
                trunk_angle=90, branch_angle=(30, 60), branch_length_coefficient=0.7,
                max_recursion_depth=7, min_branch_thickness=1, max_branch_thickness=4,
                color_function_name='natural_coloring')

    garden.set_tree_on_position(tree, 2)
    garden.index_cur_tree = 2
    garden.draw(warning_on=False)

    root.mainloop()


is_it_admin = False
window = None
garden = None
SIZE = (1280, 720)