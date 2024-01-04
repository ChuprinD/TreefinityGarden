from tkinter import *


class Window:
    def __init__(self, root, title='New window', size=(1280, 720), path_icon='', buttons=[], path_background_img='', canvases=[]):
        self.root = root
        self.root.resizable(False, False)
        self.root.iconbitmap(path_icon)
        self.root.title(title)

        self.size = size

        self.canvas = Canvas(self.root, width=size[0], height=size[1], bg='white')

        if path_background_img != '':
            self.background_img = PhotoImage(file=path_background_img)
            self.canvas.create_image(0, 0, anchor='nw', image=self.background_img)

        #self.buttons_img = [[None, None] for _ in range(len(buttons))]
        #self.buttons = [None] * len(buttons)
        self.buttons_img = {}
        self.buttons = {}
        for button in buttons:
            button_name = button['name']

            if 'path_img' in button:
                self.buttons_img[button_name] = [PhotoImage(file=button['path_img']), None]
                self.buttons[button_name] = Button(self.canvas, anchor='center', width=self.buttons_img[button_name][0].width(), height=self.buttons_img[button_name][0].height(),
                                                   borderwidth=0, image=self.buttons_img[button_name][0], command=button['command'])

                if 'path_img_under_cursor' in button:
                    self.buttons_img[button_name][1] = PhotoImage(file=button['path_img_under_cursor'])
                    self.buttons[button_name].bind('<Enter>', lambda event, cur_button_name=button_name, is_it_under_cursor=1: self.change_button_image(cur_button_name, is_it_under_cursor))
                    self.buttons[button_name].bind('<Leave>', lambda event, cur_button_name=button_name, is_it_under_cursor=0: self.change_button_image(cur_button_name, is_it_under_cursor))

                self.buttons[button_name].place(x=button['x'] - self.buttons_img[button_name][0].width() / 2,
                                                y=button['y'] - self.buttons_img[button_name][0].height() / 2)
            else:
                self.buttons[button_name] = Button(self.canvas, command=button['command'], text=button['text'], font=button['font'], width=15)
                self.buttons[button_name].place(x=button['x'] - self.buttons[button_name].winfo_reqwidth() / 2,
                                                y=button['y'] - self.buttons[button_name].winfo_reqheight() / 2)

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
            self.canvas.create_window(coords[0], coords[1], width=canvas_size[0], height=canvas_size[1], anchor='nw', window=inner_canvas)
            if 'bg_picture' in canvas:
                inner_canvas.create_image(0, 0, anchor='nw', image=self.inner_canvases_picture[name], tags='bg')

            self.inner_canvases.update({name: inner_canvas})

        self.center_window()
        self.canvas.pack()


    def change_button_image(self, button_name, is_it_under_cursor):
        self.buttons[button_name].config(image=self.buttons_img[button_name][is_it_under_cursor])

    def center_window(self):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x_coordinate = (screen_width - self.size[0]) // 2
        y_coordinate = (screen_height - self.size[1]) // 2

        self.root.geometry(f'{self.size[0]}x{self.size[1]}+{x_coordinate}+{y_coordinate}')