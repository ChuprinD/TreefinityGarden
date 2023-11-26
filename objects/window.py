from tkinter import *

class Window:
    def __init__ (self, root, title="New windwo", size=[1920, 1080], buttons=[], path_background_img="", canvases=[]):
        self.root = root
        self.root.title(title)

        self.size = size

        self.canvas = Canvas(self.root, width=size[0], height=size[1])
        if path_background_img:
            self.img = PhotoImage(file=path_background_img)
            self.canvas.create_image(0, 0, anchor="nw", image=self.img)

        self.buttons = []
        for button in buttons:
            self.buttons.append(Button(self.canvas,  text=button['text'], command=button['command'],))
            self.buttons[-1].place(x=button['x'], y=button['y'], width=button['width'], height=button['height'])

        self.inner_canvases = {}
        for canvas in canvases:
            name = canvas['name']
            coords = canvas['coords']
            if 'bg' in canvas:
                color = canvas['bg']
            else:
                color = 'black'

            canvas_size = (abs(coords[0] - coords[2]), abs(coords[1] - coords[3]))
            inner_canvas = Canvas(self.root, width=canvas_size[0], height=canvas_size[1], bg=color)
            inner_canvas.place(x=coords[0], y=coords[1], width=canvas_size[0], height=canvas_size[1])

            self.inner_canvases.update({name:inner_canvas})

