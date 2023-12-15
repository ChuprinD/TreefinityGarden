import random
import math
from tkinter import *
from tkinter import messagebox


from objects.tree import Tree


class Garden:
    def __init__(self, canvas):
        self.canvas = canvas

        self.canvas.bind('<Motion>', self.draw_hit_box)
        self.canvas.bind('<Button-1>', self.choose_tree)

        self.trees_pos = [(1 / 6, 57 / 63), (2 / 6, 59 / 63), (3 / 6, 61 / 63), (4 / 6, 59 / 63), (5 / 6, 57 / 63)]
        self.max_number_trees = 5
        self.trees = [None] * 5
        self.number_felled_trees = 0
        self.number_planted_trees = 0

        self.day_counter = 0
        self.day_label = None

        self.cur_season = 0
        self.days_in_season = 5
        self.seasons = ['Summer', 'Autumn', 'Winter', 'Spring']
        self.season_label = None
        self.season_background = None

        self.index_cur_tree = -1

    def draw_day_counter(self):
        if self.day_label is not None:
            self.day_label.destroy()

        self.day_label = Label(self.canvas, text='Day:   ' + str(self.day_counter), font=32)
        self.day_label.place(x=self.canvas.winfo_reqwidth() - self.day_label.winfo_reqwidth() - 20, y=10)

    def draw_season(self):
        if self.season_label is not None:
            self.season_label.destroy()

        if self.cur_season == 0:
            self.season_background = PhotoImage(file='./sprites/backgrounds/summer_background.png')
        elif self.cur_season == 1:
            self.season_background = PhotoImage(file='./sprites/backgrounds/autumn_background.png')
        elif self.cur_season == 2:
            self.season_background = PhotoImage(file='./sprites/backgrounds/winter_background.png')
        elif self.cur_season == 3:
            self.season_background = PhotoImage(file='./sprites/backgrounds/spring_background.png')

        self.canvas.create_image(0, 0, anchor='nw', image=self.season_background, tags='bg')

        self.season_label = Label(self.canvas, text=self.seasons[self.cur_season], font=32)
        self.season_label.place(x=15, y=10)

    def add_tree(self, tree):
        position = self.get_first_free_position()
        if position != -1:
            tree.pos = self.trees_pos[position]
            self.trees[position] = tree
            self.number_planted_trees += 1
            self.next_day()
        else:
            messagebox.showinfo("Warning", "Max amount of trees was reached")
        self.draw()

    def add_tree_from_file(self, file_name):
        tree = Tree(canvas=self.canvas)
        tree.load_tree_from_json(file_name)
        self.add_tree(tree)

    def set_tree_on_position(self, tree, positon):
        if self.trees[positon] is None:
            tree.pos = self.trees_pos[positon]
            self.trees[positon] = tree
            self.number_planted_trees += 1
            self.draw()

    def delete_tree(self):
        if self.index_cur_tree == -1:
            if self.trees.count(None) != self.max_number_trees:
                messagebox.showinfo("Warning", "Please choose a tree")
            else:
                messagebox.showinfo("Warning", "The garden is empty")
        else:
            self.trees[self.index_cur_tree] = None
            self.index_cur_tree = -1
            self.number_felled_trees += 1
            self.draw()

        self.next_day()

    def draw(self):
        self.clean_garden()
        self.draw_season()
        self.draw_day_counter()
        for tree in self.trees:
            if tree is not None:
                tree.draw()
        self.draw_arrow_over_selected_tree()

    def action(self, command):
        # only one manipulation with a tree in one day
        if self.index_cur_tree != -1:
            if command(self.trees[self.index_cur_tree]):
                self.next_day()
        elif self.trees.count(None) != self.max_number_trees:
            messagebox.showinfo("Warning", "Please choose a tree")
        else:
            messagebox.showinfo("Warning", "The garden is empty")

    def next_day(self):
        self.day_counter += 1
        if self.day_counter % self.days_in_season == 0:
            self.cur_season = (self.cur_season + 1) % len(self.seasons)
        self.draw()

    def clean_garden(self):
        # delete all stuff except background
        background = self.canvas.find_withtag('bg')
        if background:
            background_id = background[0]

            for item in self.canvas.find_all():
                if item != background_id:
                    self.canvas.delete(item)
        else:
            self.canvas.delete('all')

    def draw_hit_box(self, event):
        mouse_pos = (self.canvas.winfo_pointerx() - self.canvas.winfo_rootx(),
                     self.canvas.winfo_pointery() - self.canvas.winfo_rooty())
        for i, tree in enumerate(self.trees):
            if tree is not None:
                if tree.check_overlapping_hix_box(mouse_pos[0], mouse_pos[1]):
                    self.canvas.create_rectangle(tree.trunk_hit_box[0][0], tree.trunk_hit_box[0][1],
                                                 tree.trunk_hit_box[1][0],
                                                 tree.trunk_hit_box[1][1], width=2, tags='tree_' + str(i))
                else:
                    self.canvas.delete('tree_' + str(i))

    def choose_tree(self, event):
        mouse_pos = (self.canvas.winfo_pointerx() - self.canvas.winfo_rootx(),
                     self.canvas.winfo_pointery() - self.canvas.winfo_rooty())

        for i, tree in enumerate(self.trees):
            if tree is not None and tree.check_overlapping_hix_box(mouse_pos[0], mouse_pos[1]):
                self.index_cur_tree = i
                self.draw()

    def get_first_free_position(self) -> int:
        for pos in range(self.max_number_trees):
            if self.trees[pos] is None:
                return pos
        return -1

    def draw_arrow_over_selected_tree(self):
        if self.index_cur_tree != -1:
            arrow_x = self.trees[self.index_cur_tree].get_tree_coordinates()[0]
            arrow_y = self.canvas.winfo_reqheight() // 6
            arrow_angle = 30
            side_lines_length = 30

            self.canvas.create_line(arrow_x, arrow_y, arrow_x, 20, width=5, fill='red')
            self.canvas.create_line(arrow_x, arrow_y,
                                    arrow_x + int(math.sin(math.radians(arrow_angle)) * side_lines_length), arrow_y - int(math.cos(math.radians(arrow_angle)) * side_lines_length), width=5, fill='red')
            self.canvas.create_line(arrow_x, arrow_y,
                                    arrow_x - int(math.sin(math.radians(arrow_angle)) * side_lines_length), arrow_y - int(math.cos(math.radians(arrow_angle)) * side_lines_length), width=5, fill='red')
