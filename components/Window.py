import tkinter as tk

class Window():
    def __init__(self, title="window", full_screen = True, width = 500, height = 300):
        """make a main window

        Args:
            title (str, optional): window title. Defaults to "window".
            full_screen (bool, optional): enable full screen. Defaults to True.
            width (int, optional): used if full_screen is False. Defaults to 500.
            height (int, optional): used if full_screen is False. Defaults to 300.
        """
        self.root_ = tk.Tk()
        self.root_.title(title)
        if full_screen:
            self.root_.state("zoomed")
        else:
            self.window_.geometry(f"{width}x{height}+{self.window_.winfo_screenwidth()//2-width//2}+{self.window_.winfo_screenheight()//2-height//2}")
