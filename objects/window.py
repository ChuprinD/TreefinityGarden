from tkinter import *


class Window:
    def __init__(self, root, title='New window', size=(1280, 720), buttons=[], path_background_img='', canvases=[]):
        self.root = root
        self.root.resizable(False, False)
        self.root.title(title)

        self.size = size

        self.canvas = Canvas(self.root, width=size[0], height=size[1], bg='green')

        if path_background_img:
            self.background_img = PhotoImage(file=path_background_img)
            self.canvas.create_image(0, 0, anchor='nw', image=self.background_img)

        self.buttons_img = []
        self.buttons = []
        for button in buttons:
            if 'path_img' in button:
                self.buttons_img.append(PhotoImage(file=button['path_img']))
                self.buttons.append(Button(self.canvas, image=self.buttons_img[-1], command=button['command'],
                                           width=self.buttons_img[-1].width(), height=self.buttons_img[-1].height(),
                                           anchor='nw'))
                self.buttons[-1].place(x=button['x'] - self.buttons_img[-1].width() / 2,
                                       y=button['y'] - self.buttons_img[-1].height() / 2)
            else:
                self.buttons.append(Button(self.canvas, command=button['command'], text=button['text'], font=button['font'],
                                           width=15))
                self.buttons[-1].place(x=button['x'] - self.buttons[-1].winfo_reqwidth() / 2,
                                       y=button['y'] - self.buttons[-1].winfo_reqheight() / 2)



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

        self.center_window()

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_coordinate = (screen_width - self.size[0]) // 2
        y_coordinate = (screen_height - self.size[1]) // 2

        self.root.geometry(f"{self.size[0]}x{self.size[1]}+{x_coordinate}+{y_coordinate}")

    def check_mouse_on_inner_canvas(self):
        mouse_pos = (self.canvas.winfo_pointerx() - self.canvas.winfo_rootx(),
                     self.canvas.winfo_pointery() - self.canvas.winfo_rooty())

        for name, inner_canvas in self.inner_canvases.items():
            if (0 <= mouse_pos[0] <= inner_canvas.winfo_reqwidth() and
                    0 <= mouse_pos[1] <= inner_canvas.winfo_reqheight()):
                return name
        return 'None'