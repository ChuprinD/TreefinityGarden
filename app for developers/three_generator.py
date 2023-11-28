import tkinter as tk
import colorsys
import math


def draw_tree(canvas, x1, y1, angle, length, depth):
    global d_length, d_angle1, d_angle2, max_depth
    if depth:
        x2 = x1 + int(math.cos(math.radians(angle)) * length)
        y2 = y1 - int(math.sin(math.radians(angle)) * length)

        '''hue = (depth / max_depth) * 360
        rgb_color = colorsys.hsv_to_rgb(hue / 360, 1.0, 1.0)
        hex_color = '#%02x%02x%02x' % (int(rgb_color[0] * 255), int(rgb_color[1] * 255), int(rgb_color[2] * 255))

        canvas.create_line(x1, y1, x2, y2, fill=hex_color, width=((depth - 1) * (4 - 1)) / (max_depth - 1) + 1)'''

        #canvas.create_line(x1, y1, x2, y2, fill='chocolate', width=((depth - 1) * (4 - 1)) / (max_depth - 1) + 1)

        #color = blend_colors((34, 139, 34), (139, 69, 19), depth / max_depth)
        #color = blend_colors((254, 141, 198), (254, 209, 199), depth / max_depth)
        color = blend_colors((255, 0, 212), (0, 221, 255), depth / max_depth)
        canvas.create_line(x1, y1, x2, y2, fill=color, width=((depth - 1) * (4 - 1)) / (max_depth - 1) + 1)

        angle1 = angle + d_angle1
        angle2 = angle - d_angle2
        length *= d_length

        draw_tree(canvas, x2, y2, angle1, length, depth - 1)
        draw_tree(canvas, x2, y2, angle2, length, depth - 1)


def blend_colors(color1, color2, ratio):
    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
    return f'#{r:02x}{g:02x}{b:02x}'


def get_slider_value(*args):
    global d_angle1, d_angle2, d_length, max_depth
    canvas.delete('all')
    d_angle1 = slider_angle1.get()
    d_angle2 = slider_angle2.get()
    depth = slider_depth.get()
    max_depth = depth
    d_length = slider_length.get()
    trunk_length = slider_trunk.get()
    draw_tree(canvas, start_x, start_y, trunk_angle, trunk_length, depth)

root = tk.Tk()
root.title("Fractal tree")
WIDTH = 800
HEIGHT = 800
canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")

start_x, start_y = WIDTH / 2, HEIGHT - 10
trunk_angle = 90
max_deph = 0

trunk_length = 0
slider_trunk = tk.Scale(root, from_=0, to=300, command=get_slider_value, orient=tk.HORIZONTAL)
slider_trunk.pack()
slider_trunk.place(x=WIDTH - 100, y=210)
label_trunk = tk.Label(root, text="trunk_length")
label_trunk.place(x=WIDTH - 170, y=230)

d_length = 0.7
slider_length = tk.Scale(root, from_=0, to=1, command=get_slider_value, resolution=0.005, orient=tk.HORIZONTAL)
slider_length.pack()
slider_length.place(x=WIDTH - 100, y=160)
label_length = tk.Label(root, text="d_length")
label_length.place(x=WIDTH - 150, y=180)

depth = 0
slider_depth = tk.Scale(root, from_=2, to=15, command=get_slider_value, orient=tk.HORIZONTAL)
slider_depth.pack()
slider_depth.place(x=WIDTH - 100, y=110)
label_depth = tk.Label(root, text="depth")
label_depth.place(x=WIDTH - 150, y=130)

d_angle1 = 0
slider_angle1 = tk.Scale(root, from_=-90, to=90, command=get_slider_value, orient=tk.HORIZONTAL)
slider_angle1.pack()
slider_angle1.place(x=WIDTH - 100, y=10)
label_angle1 = tk.Label(root, text="d_angle1")
label_angle1.place(x=WIDTH - 150, y=30)

d_angle2 = 0
slider_angle2 = tk.Scale(root, from_=-90, to=90, command=get_slider_value, orient=tk.HORIZONTAL)
slider_angle2.pack()
slider_angle2.place(x=WIDTH - 100, y=60)
label_angle2 = tk.Label(root, text="d_angle2")
label_angle2.place(x=WIDTH - 150, y=80)

canvas.pack()
root.mainloop()
