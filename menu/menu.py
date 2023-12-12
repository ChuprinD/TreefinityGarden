from tkinter import *

from game.game import run_game
from objects.window import Window


def close_menu_run_game(root):
    root.destroy()
    run_game()


def run_menu():
    root = Tk()
    root.iconbitmap('./sprites/icon.ico')

    WIDTH = 420
    HEIGHT = 720
    x_coordinate = (root.winfo_screenwidth() - WIDTH) // 2
    y_coordinate = (root.winfo_screenheight() - HEIGHT) // 2
    root.geometry(f'{WIDTH // 3 + 30}x{HEIGHT // 2}+{x_coordinate}+{y_coordinate}')

    buttons = [{'x': WIDTH / 2, 'y': HEIGHT * 2 / 5, 'text': 'Start', 'font': ('Arial', 20, 'bold'),
                'command': lambda: close_menu_run_game(root)},
               {'x': WIDTH / 2, 'y': HEIGHT * 2 / 5 + HEIGHT / 10, 'text': 'Skins', 'font': ('Arial', 20, 'bold'),
                'command': lambda: print('lol')},
               {'x': WIDTH / 2, 'y': HEIGHT * 2 / 5 + HEIGHT / 5, 'text': 'Achievements', 'font': ('Arial', 20, 'bold'),
                'command': lambda: print('kek')}]

    window = Window(root, title='Treefinity Garden', size=[WIDTH, HEIGHT],
                    path_background_img='./sprites/backgrounds/window_background.png', buttons=buttons)

    icon = PhotoImage(file='./sprites/icon.png')
    window.canvas.create_image(WIDTH / 15, HEIGHT / 7, anchor='nw', image=icon)

    name_of_project = Label(window.canvas, text='Treefinity Garden', font=('Arial', 25))
    name_of_project.place(x=WIDTH / 3 + 5, y=HEIGHT / 6 + 10)

    window.canvas.pack()
    root.mainloop()
