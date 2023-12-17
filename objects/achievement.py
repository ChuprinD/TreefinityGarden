from tkinter import messagebox


class Achievement:
    def __init__(self, is_it_unlock, condition):
        self.is_it_unlock = is_it_unlock
        self.condition = condition

    def check_condition(self):
        if self.condition() and self.is_it_unlock == False:
            messagebox.showinfo('Achievement unlocked', 'You\'ve unlocked a new skin for the tree')
            self.is_it_unlock = True

        return self.is_it_unlock
