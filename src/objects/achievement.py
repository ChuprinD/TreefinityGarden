from tkinter import *
from tkinter import messagebox


class Achievement:
    def __init__(self, id, name, is_it_unlock, condition, unlocked_tree):
        self.id = id
        self.name = name
        self.image = None
        self.is_it_unlock = is_it_unlock
        self.condition = condition
        self.unlocked_tree = unlocked_tree

    def check_condition(self):
        if self.condition() and not self.is_it_unlock:
            messagebox.showinfo('Achievement unlocked', self.name + '\nYou\'ve unlocked a new skin')
            self.is_it_unlock = True

        return self.is_it_unlock

    def set_image(self, image_path):
        self.image = PhotoImage(file=image_path)

