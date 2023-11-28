from tkinter import *
from objects.tree import Tree
from objects.window import Window
from objects.garden import Garden
from utilities.color import *



def create_slider(parent, update_callback, minimum, maximum, pos, initial_value, label_text, ratio=1):
    label = Label(parent, text=label_text)
    label.place(x=pos[0] - label.winfo_reqwidth(), y=pos[1])

    slider = Scale(parent, from_=minimum, to=maximum, orient="horizontal", command=update_callback,
                   variable=DoubleVar(value=initial_value), resolution=ratio, length=300)
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

root = Tk()
root.title('DEV APP')
WIDTH = 1920
HEIGHT = 1080

window = Window(root, title='Treefinity Garden', size=[WIDTH, HEIGHT],
                path_background_img='../sprites/window_background.png',
                canvases=[{'name': 'garden', 'coords': (30, 30, 1350, 1050), 'bg': 'blue',
                           'bg_picture': '../sprites/garden_background.png'}])

garden = Garden(canvas=window.inner_canvases['garden'])

tree = Tree(canvas=window.inner_canvases['garden'],
            pos=(window.inner_canvases['garden'].winfo_reqwidth() / 2,
                 window.inner_canvases['garden'].winfo_reqheight() - 30),
            trunk_length=200, trunk_angle=90, branch_angle=(30, 60), branch_length_coefficient=0.7,
            max_recursion_depth=7, min_branch_thickness=1,
            max_branch_thickness=4, color_function=neon_coloring)

slider_trunk_length = create_slider(parent=window.canvas, minimum=0, maximum=400,
                             update_callback=update_trunk_length, pos=(1550, 30),
                             label_text='trunk_length', initial_value=tree.trunk_length)

slider_branch_length_coefficient = create_slider(parent=window.canvas, minimum=0, maximum=1,
                             update_callback=update_branch_length_coefficient, pos=(1550, 90), ratio=0.005,
                             label_text='branch_length_coefficient', initial_value=tree.branch_length_coefficient)

slider_max_recursion_depth = create_slider(parent=window.canvas, minimum=2, maximum=15,
                             update_callback=update_max_recursion_depth, pos=(1550, 150),
                             label_text='max_recursion_depth', initial_value=tree.max_recursion_depth)

slider_branch__angle1 = create_slider(parent=window.canvas, minimum=-90, maximum=90,
                             update_callback=update_branch_angle1, pos=(1550, 210),
                             label_text='max_trunk_angle1', initial_value=tree.branch_angle[0])

slider_branch__angle2 = create_slider(parent=window.canvas, minimum=-90, maximum=90,
                             update_callback=update_branch_angle2, pos=(1550, 270),
                             label_text='max_trunk_angle1', initial_value=tree.branch_angle[1])

garden.add_tree(tree)
garden.draw()

window.canvas.pack()
root.mainloop()
