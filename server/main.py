from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
from threading import Thread
from recipient import Recipient


APP_TITLE = 'Online ASCII-art'
BACKGROUND_COLOR = 'white'
IMG_INITIAL_WIDTH = 1200
IMG_INITIAL_HEIGHT = 800

class ServerApp():
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title(APP_TITLE)
        self.frame = Frame(self.main_window)

        self.img_width = IMG_INITIAL_WIDTH
        self.img_height = IMG_INITIAL_HEIGHT
        self.background_color = BACKGROUND_COLOR

        self._init_canvas()

        ascii_listener = Thread(target=self.show_ascii)
        ascii_listener.start()

    def _init_canvas(self):
        self.canvas = Canvas(self.main_window, bg=self.background_color)
        self.canvas.pack(expand=1, fill=BOTH)

        self.img = Image.new('RGB', [self.img_width, self.img_height], self.background_color)

        self.canvas.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor=NW, image=self.canvas.img)

        self.canvas.bind('<Configure>', self.configure)
        
    def configure(self, event):
        self.canvas.delete('all')
        self.img_width = event.width
        self.img_height = event.height

        self.img = self.img.resize((self.img_width, self.img_height))

        self.canvas.img = ImageTk.PhotoImage(self.img)
        self.canvas.create_image(0, 0, anchor=NW, image=self.canvas.img)

    def show_ascii(self):
        recipient = Recipient()

        while True:
            self.img = recipient.receive_images()

            self.canvas.img = ImageTk.PhotoImage(self.img)
            self.canvas.create_image(0, 0, anchor=NW, image=self.canvas.img)





if __name__ == '__main__':
    main_window = Tk()
    main_window.geometry(f'{IMG_INITIAL_WIDTH}x{IMG_INITIAL_HEIGHT}')
    main_window.style = ttk.Style()
    main_window.style.theme_use('clam')

    app = ServerApp(main_window)
    main_window.mainloop()