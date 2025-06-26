import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from components.Window import Window
import os
from components.QRGenerator import QRGenerator
from components.CSVLoader import CSVLoader

class InputUI():
    def __init__(self, title: str = "QR code generator", full_screen: bool = True, width: int = 500, height: int = 300):
        """make a main window

        Args:
            title (str, optional): window title. Defaults to "window".
            full_screen (bool, optional): enable full screen. Defaults to True.
            width (int, optional): used if full_screen is False. Defaults to 500.
            height (int, optional): used if full_screen is False. Defaults to 300.
        """
        self.window_ = Window(title, full_screen, width, height)
        self.window_.root_.minsize(width = 300, height = 500)
        self.make_ui()

    def make_ui(self):
        """make ui for user
        """
        font = ("Arial", 20)
        subfont = ("Arial", 16)

        main_frame = ttk.Frame(self.window_.root_, padding=20)
        main_frame.pack(expand=True)

        # make a dialog to select qr data csv file
        self.qr_data_file_label_ = tk.Label(main_frame, text="QR csv file", font=font)
        self.qr_data_file_label_.pack(anchor="center")
        file_frame = ttk.Frame(main_frame)
        file_frame.pack(pady=10)
        self.qr_data_file_entry_ = tk.StringVar()
        qr_data_file_dialog = ttk.Entry(file_frame, textvariable=self.qr_data_file_entry_, width=40, font=subfont)
        qr_data_file_dialog.pack(side="left", padx=5)
        self.qr_data_file_refer_ = tk.Button(file_frame, text="Ref", command=self.clicked_filedialog, font=subfont)
        self.qr_data_file_refer_.pack(side="left", padx=5)

        # make a dialog to select save directory for qr code images
        self.qr_save_dir_label_ = tk.Label(main_frame, text="QR code directory for save", font=font)
        self.qr_save_dir_label_.pack(anchor="center")
        dir_frame = ttk.Frame(main_frame)
        dir_frame.pack(pady=10)
        self.qr_save_dir_entry_ = tk.StringVar()
        qr_save_dir_dialog = ttk.Entry(dir_frame, textvariable=self.qr_save_dir_entry_, width=40, font=subfont)
        qr_save_dir_dialog.pack(side="left", padx=5)
        self.qr_save_dir_refer_ = tk.Button(dir_frame, text="Ref", command=self.clicked_dirdialog, font=subfont)
        self.qr_save_dir_refer_.pack(side="left", padx=5)

        # generation button
        submit_button = tk.Button(main_frame, text="OK", command=self.on_submit, font=font)
        submit_button.pack(pady=20)

        # button to see something
        usage_button = tk.Button(self.window_.root_, text="Usage", command=self.show_usage, font = ("Arial", 15))
        usage_button.place(relx=1.0, rely=1.0, anchor='se', x=-130, y=-30)
        attention_button = tk.Button(self.window_.root_, text="Attention", command=self.show_attention, font = ("Arial", 15))
        attention_button.place(relx=1.0, rely=1.0, anchor='se', x=-30, y=-30)

        
    def focus_next_widget(self, event):
        """ go to next widget
        """
        event.widget.tk_focusNext().focus()
        return "break"
    
    def show_usage(self):
        """show usage
        """
        usage_msg = "Usage\n\n1. Choose a csv file\n2. Choose a save directory.\n3. OK"
        messagebox.showinfo("Usage", usage_msg)

    def show_attention(self):
        """show attention message
        """
        attention_msg = "Attention\n\n\
・csv file includes a header which consists of \"file_name\" and \"qr_data\"."
        messagebox.showwarning("Attention", attention_msg)
 
    def clicked_dirdialog(self):
        dirpath = os.path.abspath(os.path.dirname(__file__))
        dirpath = filedialog.askdirectory(initialdir = dirpath)
        self.qr_save_dir_entry_.set(dirpath)
 
    def clicked_filedialog(self):
        fTyp = [("", "*")]
        filepath = os.path.abspath(os.path.dirname(__file__))
        filepath = filedialog.askopenfilename(filetype = fTyp, initialdir = filepath)
        self.qr_data_file_entry_.set(filepath)
 
    def submit_on_enter(self, event):
        """hadle enter key
        """
        self.on_submit()
        return "break"
    
    def on_submit(self):
        """handle button action
        """
        # check required info
        qr_data_csv_file_path = self.qr_data_file_entry_.get()
        save_folder_path = self.qr_save_dir_entry_.get()
        if qr_data_csv_file_path == "" or save_folder_path == "":
            messagebox.showerror('Error', 'Input all required parameters.')
            return
        if qr_data_csv_file_path.split(".")[-1] != "csv":
            messagebox.showerror('Error', 'Choose csv file.')
            return
        print(f"qr data file path: {qr_data_csv_file_path}")
        print(f"save folder path: {save_folder_path}")
        csv_loader = CSVLoader()
        qr_generator = QRGenerator()
        [qr_img_name_list, qr_data_list], error_code = csv_loader.get_shaped_data(qr_data_csv_file_path)
        if error_code != None:
            messagebox.showerror('Error', 'The csv file you chose does not follow the designated format. Refer to the attention popup.')
            self.show_attention()
            return
        for img_name, data in zip(qr_img_name_list, qr_data_list):
            print(f"generate {img_name}.png \n\twith data {data}")
            qr_img = qr_generator.generate(data)
            qr_img.save(os.path.join(save_folder_path, f"{img_name}.png"))

        print("successfully generated and saved")
        messagebox.showinfo('Infomation', 'QR codes are generated.')
