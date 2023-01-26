
from res.constants import *


class Window:
    def __init__(self, parent):
        self.window = parent
        self.window.title(APP_TITLE)
        self.window.resizable(False, False)
        self.window.geometry(APP_DIMS_COMPACT)



if __name__ == "__main__":
    root = tk.Tk()
    Window(root)
    root.mainloop()
