
from res.constants import *
from res.interface import *


class Window:
    def __init__(self, parent):
        self.window = parent
        self.window.title(APP_TITLE)
        self.window.resizable(False, False)
        self.window.geometry(APP_DIMS_COMPACT)

    def home_page(self):
        home_frame = make_frame(self.window, MAIN_BG, 1, 1, 0.5, 0.5, "center")

        make_label(home_frame, "WELCOME", MAIN_BG, TITLE_FG, 0.5, 0.03, "n", 20)

        make_img_button(home_frame, "", 200, 200, BUTTON_BG, "black", 0, 0.5, "w", lambda: self.recommend_preset_page(), 12, SEARCH_ICON_DIR)
        make_label(home_frame, "Recommend Preset", MAIN_BG, LABEL_FG, 0.125, 0.86, "center", 14)

        make_img_button(home_frame, "", 200, 200, BUTTON_BG, "black", 0.25, 0.5, "w", lambda: self.manage_preset_page(), 12, TICK_ICON_DIR)
        make_label(home_frame, "Select Preset", MAIN_BG, LABEL_FG, 0.375, 0.86, "center", 14)

        make_img_button(home_frame, "", 200, 200, BUTTON_BG, "black", 0.5, 0.5, "w", lambda: self.create_preset_page(), 12, ADD_ICON_DIR)
        make_label(home_frame, "Create Preset", MAIN_BG, LABEL_FG, 0.625, 0.86, "center", 14)

        make_img_button(home_frame, "", 200, 200, BUTTON_BG, "black", 0.75, 0.5, "w", lambda: quit(), 12, EXIT_ICON_DIR)
        make_label(home_frame, "Quit", MAIN_BG, LABEL_FG, 0.875, 0.86, "center", 14)




if __name__ == "__main__":
    root = tk.Tk()
    Window(root)
    root.mainloop()
