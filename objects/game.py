from tkinter import *

class Garden:
    def __init__(self, canvas):
        self.canvas = canvas

        self.trees = []

        self.day_counter = 0
        self.day_label = None

        self.cur_season = 0
        self.days_in_season = 5
        self.seasons = ["Summer", "Autumn", "Winter", "Spring"]
        self.season_label = None

        self.index_cur_tree = 0



    def draw_day_counter(self):
        if self.day_label is not None:
            self.day_label.destroy()
            
        self.day_label = Label(self.canvas, text="Day:   " + str(self.day_counter), font=32)
        self.day_label.place(x=self.canvas.winfo_reqwidth() - self.day_label.winfo_reqwidth() - 30, y=10)

    def draw_season(self):
        if self.season_label is not None:
            self.season_label.destroy()

        self.season_label = Label(self.canvas, text=str(self.seasons[self.cur_season]), font=32)
        self.season_label.place(x=self.canvas.winfo_reqwidth() / 2 - self.season_label.winfo_reqwidth(), y=10)

    def add_tree(self, tree):
        self.trees.append(tree)

    def draw(self):
        self.canvas.delete('all')
        for tree in self.trees:
            tree.draw()
        self.draw_day_counter()
        self.draw_season()

    def action(self, command):
        command(self.trees[self.index_cur_tree])
        self.day_counter += 1
        if self.day_counter % self.days_in_season == 0:
            self.cur_season = (self.cur_season + 1) % len(self.seasons)
        self.draw()



