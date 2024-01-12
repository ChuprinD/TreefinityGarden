from tkinter import *

from src.objects.window import Window


def close_achievements(root):
    from src.menu.menu import run_menu
    root.destroy()
    run_menu()


def run_achievements(player):
    root = Tk()
    root.protocol('WM_DELETE_WINDOW', lambda: close_achievements(root))

    WIDTH = 420
    HEIGHT = 720

    window = Window(root, title='Achievements', size=[WIDTH, HEIGHT], path_icon='resources/sprites/icon.ico', path_background_img='resources/sprites/backgrounds/window_background.png')

    path_to_achievements = 'resources/sprites/achievements/'

    achievements = {
        'Grew your first tree':      [path_to_achievements + 'open_achievements/first_tree.png',         path_to_achievements + 'close_achievements/first_tree.png'],
        'Plant your third tree':     [path_to_achievements + 'open_achievements/three_trees.png',        path_to_achievements + 'close_achievements/three_trees.png'],
        'Killed your first tree )=': [path_to_achievements + 'open_achievements/killed_first_tree.png',  path_to_achievements + 'close_achievements/killed_first_tree.png'],
        'Killed your third tree )=': [path_to_achievements + 'open_achievements/killed_third_tree.png',  path_to_achievements + 'close_achievements/killed_third_tree.png'],
        'Maxxed out garden!':        [path_to_achievements + 'open_achievements/maxed_garden.png',       path_to_achievements + 'close_achievements/maxed_garden.png'],
        'Made it through winter!':   [path_to_achievements + 'open_achievements/winter.png',             path_to_achievements + 'close_achievements/winter.png'],
        'Made it to day 365!':       [path_to_achievements + 'open_achievements/1_year.png',             path_to_achievements + 'close_achievements/1_year.png'],
        'Unlocked all skins!':       [path_to_achievements + 'open_achievements/unlocked_all_skins.png', path_to_achievements + 'close_achievements/unlocked_all_skins.png'],
        'Killed all trees )=':       [path_to_achievements + 'open_achievements/killed_all_trees.png',   path_to_achievements + 'close_achievements/killed_all_trees.png'],
        'Mystery':                   [path_to_achievements + 'open_achievements/mystery.png',            path_to_achievements + 'close_achievements/mystery.png']
    }

    for achievement in player.all_achievements:
        if achievement.name in achievements:
            achievement.set_image(achievements[achievement.name][1 - achievement.is_it_unlock])

    for i, achievement in enumerate(player.all_achievements):
        window.canvas.create_image(50, 46 + i * 60, image=achievement.image, anchor='nw')

        for dx, dy in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
            window.canvas.create_text(200 + dx, 60 + i * 60 + dy, text=achievement.name, anchor='nw', fill='black', font=('Impact', 15))

        achievement_color = '#AEB5BF'
        if achievement.is_it_unlock:
            achievement_color = 'yellow'

        window.canvas.create_text(200, 60 + i * 60, text=achievement.name, anchor='nw', fill=achievement_color, font=('Impact', 15))



    window.root.mainloop()
