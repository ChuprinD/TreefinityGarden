from tkinter import *


class Window:
    def __init__(self, root, title='New window', size=(1920, 1080), buttons=[], path_background_img='', canvases=[]):
        self.root = root
        self.root.title(title)

        self.size = size

        self.canvas = Canvas(self.root, width=size[0], height=size[1])

        if path_background_img:
            self.background_img = PhotoImage(file=path_background_img)
            self.canvas.create_image(0, 0, anchor='nw', image=self.background_img)

        self.buttons_img = []
        self.buttons = []
        for button in buttons:
            self.buttons_img.append(PhotoImage(file=button['path_img']))
            self.buttons.append(Button(self.canvas, command=button['command'], image=self.buttons_img[-1],
                                       width=self.buttons_img[-1].width(), height=self.buttons_img[-1].height(),
                                       anchor='nw'))
            self.buttons[-1].place(x=button['x'] - self.buttons_img[-1].width() / 2,
                                   y=button['y'] - self.buttons_img[-1].height() / 2)

        self.inner_canvases = {}
        self.inner_canvases_picture = {}
        for canvas in canvases:
            name = canvas['name']
            coords = canvas['coords']
            if 'bg_picture' in canvas:
                image = PhotoImage(file=canvas['bg_picture'])
                self.inner_canvases_picture.update({name: image})
            if 'bg' in canvas:
                color = canvas['bg']
            else:
                color = 'black'

            canvas_size = (abs(coords[0] - coords[2]), abs(coords[1] - coords[3]))
            inner_canvas = Canvas(self.root, width=canvas_size[0], height=canvas_size[1], bg=color)
            inner_canvas.place(x=coords[0], y=coords[1], width=canvas_size[0], height=canvas_size[1])
            if 'bg_picture' in canvas:
                inner_canvas.create_image(0, 0, anchor='nw', image=self.inner_canvases_picture[name], tags='bg')

            self.inner_canvases.update({name: inner_canvas})