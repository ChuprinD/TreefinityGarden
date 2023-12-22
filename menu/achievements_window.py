from tkinter import *

from objects.window import Window


def close_achievements(root):
    from menu.menu import run_menu
    root.destroy()
    run_menu()


def run_achievements():
    root = Tk()
    root.protocol('WM_DELETE_WINDOW', lambda: close_achievements(root))

    WIDTH = 420
    HEIGHT = 720

    window = Window(root, title='Achievements', size=[WIDTH, HEIGHT], path_icon='./sprites/icon.ico', path_background_img='./sprites/backgrounds/window_background.png')

    achievements = [
        'Grew your first tree',
        'Grew your third tree',
        'Killed your first tree ):',
        'Killed your third tree ):',
        'Maxxed out garden!',
        'Made it through winter!',
        'Made it to day 365!',
        'Unlocked all skins!',
        'Killed all trees ):',
        'Mystery',
    ]

    for i, achievement in enumerate(achievements):
        window.canvas.create_rectangle(50, 30 + i * 60, 150, 80 + i * 60, fill='darkgrey', outline='black')

        label = Label(root, text=achievement)
        label.place(x=200, y=50 + i * 60, anchor='w')

    window.root.mainloop()
