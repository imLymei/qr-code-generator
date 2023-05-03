import tkinter as tk
from tkinter import filedialog
import customtkinter as ctk
from PIL import ImageTk
import qrcode

try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color='white')

        ctk.set_appearance_mode('light')
        self.title('')
        self.geometry('400x400')
        self.iconbitmap('./src/empty.ico')
        self.resizable(False, False)

        self.title_bar_color()

        self.entry_string = tk.StringVar()
        self.entry_string.trace('w', self.create_qr)
        EntryField(self, self.entry_string, self.save)

        self.bind_all('<Return>', self.save)

        self.raw_image = None
        self.tk_image = None
        self.qr_code = QrImage(self)

        self.mainloop()

    def create_qr(self, *args):
        current_text = self.entry_string.get()

        if current_text:
            self.raw_image = qrcode.make(current_text)
            self.tk_image = ImageTk.PhotoImage(self.raw_image.resize((160, 160)))
            self.qr_code.update_image(self.tk_image)
        else:
            self.qr_code.clear()
            self.raw_image = None
            self.tk_image = None

    def save(self, event=None):
        if self.raw_image:
            file_name = filedialog.asksaveasfilename(defaultextension='.png')
            if file_name:
                self.raw_image.save(file_name)

    def title_bar_color(self):
        try:
            HWND = windll.user32.GetParent(self.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(HWND, 35, byref(c_int(0x00FFFFFF)),
                                                sizeof(c_int))
        except:
            pass


class EntryField(ctk.CTkFrame):
    def __init__(self, master, entry_var, button_command):
        super().__init__(master, corner_radius=20, fg_color='#021FB3')
        self.place(relx=0.5, rely=1, relwidth=1,
                   relheight=0.4, anchor='center')

        self.rowconfigure((0, 1), weight=1, uniform='a')
        self.columnconfigure(0, weight=1, uniform='a')

        self.frame = ctk.CTkFrame(self, fg_color='transparent')
        self.frame.rowconfigure(0, weight=1, uniform='b')
        self.frame.columnconfigure(0, weight=1, uniform='b')
        self.frame.columnconfigure(1, weight=4, uniform='b')
        self.frame.columnconfigure(2, weight=2, uniform='b')
        self.frame.columnconfigure(3, weight=1, uniform='b')
        self.frame.grid(row=0, column=0)

        entry = ctk.CTkEntry(self.frame, fg_color='#2E54E8',
                             border_width=0, text_color='white',
                             textvariable=entry_var)
        entry.grid(row=0, column=1, sticky='nswe', padx=10)

        button = ctk.CTkButton(self.frame, text='save',
                               fg_color='#2E54E8', hover_color='#4266F1',
                               command=button_command)
        button.grid(row=0, column=2, sticky='nswe', padx=10)


class QrImage(tk.Canvas):
    def __init__(self, master):
        super().__init__(master, background='white', bd=0,
                         highlightthickness=0, relief='ridge')
        self.place(relx=0.5, rely=0.4, relwidth=0.4, relheight=0.4, anchor='center')

    def update_image(self, image_tk):
        self.clear()
        self.create_image(0, 0, image=image_tk, anchor='nw')

    def clear(self):
        self.delete('all')


if __name__ == '__main__':
    App()
