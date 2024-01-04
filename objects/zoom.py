from tkinter import *
from tkinter import messagebox


class Zoom:
    def __init__(self, garden, zoom_delta):
        self.garden = garden
        self.is_zoom_activated = False
        self.cur_zoom = 1
        self.max_zoom = zoom_delta ** 4
        self.zoom_delta = zoom_delta
        self.prev_mouse_pos = []

    def set_binds(self):
        self.garden.canvas.bind('<Button-1>', lambda event: self.zoom_in(event))
        self.garden.canvas.bind('<Button-3>', lambda event: self.zoom_out(event))

    def remove_binds(self):
        self.garden.canvas.unbind('<Button-1>')
        self.garden.canvas.unbind('<Button-3>')


    def activate_zoom(self, window):
        self.garden.remove_binds()
        self.garden.delete_arrow_over_selected_tree()
        self.set_binds()
        self.prev_mouse_pos.clear()

        window.buttons_img['magnifier'] = [PhotoImage(file='./sprites/buttons/regular_buttons/magnifier_on.png'),
                                           PhotoImage(file='./sprites/buttons/under_cursor_buttons/magnifier_on.png')]
        window.buttons['magnifier'].config(image=window.buttons_img['magnifier'][0], command=lambda: self.deactivate_zoom(window))

        self.is_zoom_activated = True
        messagebox.showinfo('Zoom activated', 'Left-click: Zoom In\nRight-click: Zoom Out')

    def deactivate_zoom(self, window):
        self.remove_binds()
        self.garden.set_binds()

        while self.cur_zoom != 1:
            self.zoom((0, 0), 1 / self.zoom_delta)
        window.buttons_img['magnifier'] = [PhotoImage(file='./sprites/buttons/regular_buttons/magnifier_off.png'),
                                           PhotoImage(file='./sprites/buttons/under_cursor_buttons/magnifier_off.png')]
        window.buttons['magnifier'].config(image=window.buttons_img['magnifier'][0], command=lambda: self.activate_zoom(window))

        self.is_zoom_activated = False
        messagebox.showinfo('Zoom deactivated', 'Zoom successfully deactivated')

    def zoom_in(self, event):
        if self.cur_zoom * self.zoom_delta > self.max_zoom:
            return

        mouse_pos = (event.x, event.y)
        self.zoom(mouse_pos, self.zoom_delta)

    def zoom_out(self, event):
        if self.cur_zoom == 1:
            return

        mouse_pos = (event.x, event.y)
        self.zoom(mouse_pos, 1 / self.zoom_delta)

    def zoom(self, center, ratio):
        if self.cur_zoom == 1:
            self.prev_mouse_pos.clear()

        self.garden.clean_garden()

        if ratio >= 1:
            self.garden.season_background = self.garden.season_background.zoom(self.zoom_delta)
        else:
            self.garden.season_background = self.garden.season_background.subsample(self.zoom_delta)

        self.garden.canvas.create_image(0, 0, anchor='nw', image=self.garden.season_background, tags='bg')

        for tree in self.garden.trees:
            if tree is not None:
                tree.draw(False)

        if len(self.prev_mouse_pos) != 0:
            # since scale works as a homotopy to a point, here I calculate the center of the homotopy composition
            cur_zoom_center_x = sum(point[0] for point in self.prev_mouse_pos) / len(self.prev_mouse_pos)
            cur_zoom_center_y = sum(point[1] for point in self.prev_mouse_pos) / len(self.prev_mouse_pos)

            self.garden.canvas.scale('all', cur_zoom_center_x + (center[0] - cur_zoom_center_x) / self.cur_zoom,
                                     cur_zoom_center_y + (center[1] - cur_zoom_center_y) / self.cur_zoom,
                                     int(self.cur_zoom * ratio), int(self.cur_zoom * ratio))
        else:
            self.garden.canvas.scale('all', center[0], center[1], int(self.cur_zoom * ratio), int(self.cur_zoom * ratio))

        self.cur_zoom = int(self.cur_zoom * ratio)
        self.prev_mouse_pos.append(center)
