from tkinter import Tk, Canvas, Label


def run_achievements():
    root = Tk()
    root.iconbitmap('./sprites/icon.ico')
    root.protocol("WM_DELETE_WINDOW", lambda: root.destroy())

    WIDTH = 420
    HEIGHT = 720
    x_coordinate = (root.winfo_screenwidth() - WIDTH) // 2
    y_coordinate = (root.winfo_screenheight() - HEIGHT) // 2

    root.geometry(f'{WIDTH}x{HEIGHT}+{x_coordinate}+{y_coordinate}')
    root.title('Achievements')

    canvas = Canvas(root, width=WIDTH, height=HEIGHT, bg='white')
    canvas.pack()

    achievements = [
        "Grew your first tree",
        "Grew your third tree",
        "Killed your first tree ):",
        "Killed your third tree ):",
        "Maxxed out garden!",
        "Made it through winter!",
        "Made it to day 365!",
        "Unlocked all skins!",
        "Killed all trees ):",
        "Mystery",
    ]

    for i, achievement in enumerate(achievements):
        canvas.create_rectangle(50, 30 + i*60, 150, 80 + i*60, fill='darkgrey', outline='black')

        label = Label(root, text=achievement)
        label.place(x=200, y=50 + i * 60, anchor='w')  # Adjust the coordinates as needed

    root.mainloop()
