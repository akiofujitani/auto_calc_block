import logging
import tkinter
from tkinter import scrolledtext
from tkinter import messagebox
from copy import deepcopy
from .json_config import save_json_config
from .support_funcions import save_config_on_change
from .file_handler import resource_path
from .classes.config import Configuration, GuiConfiguration
from .gui_builder import About
from queue import Queue
from PIL import Image, ImageTk

logger = logging.getLogger('gui')


class MainApp(tkinter.Tk):
    def __init__(self, title: str, log_queue: Queue, config: Configuration, gui_config: GuiConfiguration, *args, **kwargs) -> None:
        tkinter.Tk.__init__(self, *args, **kwargs)
        self.title(title)
        self.log_queue = log_queue
        self.config_values = config
        self.gui_config = gui_config
        self.minsize(350, 250)

        # If config has window size and position, set it in app        
        win_pos = gui_config.check_win_pos('main')
        if win_pos:
            self.geometry(win_pos)
        
        try:
            self.icon_path = resource_path('./Icon/walrus.png')
            icon = Image.open(self.icon_path)
            icon.resize((96, 96), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(icon)
            self.wm_iconphoto(True, photo)
        except Exception as error:
            logger.error(f'Could not load icon {error}')

        # Configure grid columns weight (follow resize)        
        self.columnconfigure(0, weight=1, minsize=80)

        # Menu bar creation
        menu_bar = tkinter.Menu(self)
        file_menu = tkinter.Menu(menu_bar, tearoff=0)
        help_menu = tkinter.Menu(menu_bar, tearoff=0)
        edit_menu = tkinter.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Exit     ', command=self.__quit_window)
        edit_menu.add_command(label='Settings', command=self.__configuration)
        help_menu.add_command(label='About     ', command=self.__about_command)
        menu_bar.add_cascade(label='File     ', menu=file_menu)
        menu_bar.add_cascade(label='Edit     ', menu=edit_menu)
        menu_bar.add_cascade(label='Help     ', menu=help_menu)
        self.config(menu=menu_bar)

        # Top frame
        top_frame = tkinter.Frame(self)
        top_frame.grid(column=0, row=0, padx=(3), pady=(3), sticky='nesw')
        top_frame.columnconfigure(0, weight=1, minsize=80)
        top_frame.rowconfigure(1, weight=1, minsize=35)

        tkinter.Label(top_frame, text='Insert job number and press Ok').grid(column=0, row=0, padx=(3), pady=(3))
        self.entry_job = tkinter.Entry(top_frame, width=100, justify='center')
        self.entry_job.grid(column=0, row=1, rowspan=1, padx=(5), pady=(3), sticky='nesw')
        self.ok_button = tkinter.Button(top_frame, text='Ok', command=self.__click_button_ok, width=10)
        self.ok_button.grid(column=2, row=1, columnspan=2, padx=(5), pady=(3), sticky='nesw')

        log_frame = tkinter.Frame(self)
        log_frame.grid(column=0, row=2, columnspan=4, padx=(5), pady=(3), sticky='nesw')
        log_frame.columnconfigure(0, weight=1, minsize=80)
        log_frame.rowconfigure(0, weight=2, minsize=50)

        self.scrolled_text = scrolledtext.ScrolledText(log_frame, state='disabled')
        self.scrolled_text.configure(wrap=tkinter.WORD, font=('Arial', 9))
        self.scrolled_text.grid(column=0, row=0, columnspan=4, sticky='nesw', padx=(5), pady=(3))

        self.protocol('WM_DELETE_WINDOW', self.__on_window_close)

    def __click_button_ok(self):
        pass

    def __configuration(self):
        logger.debug('Settings')
        pass

    def __on_window_close(self):
        self.__quit_window()

    def __quit_window(self):
        if messagebox.askokcancel('Quit', 'Do you want to quit?'):
            gui_config_copy = deepcopy(self.gui_config)
            self.gui_config.update_win_size_pos(self.geometry(), 'main')
            if not self.gui_config.__eq__(gui_config_copy):
                save_json_config('gui_config.json', self.gui_config.to_dict)
            logger.info('Forcing kill thread if it is open')
            self.after(150, self.deiconify)
            self.destroy()

    def __about_command(self):
        logger.info('About clicked')
        self.about = About(self, 1,
            'About', '''
            Application name: Directory Monitor
            Version: 0.10.00
            Developed by: Akio Fujitani
            e-mail: akiofujitani@gmail.com
        ''', resource_path('./Icon/Bedo.jpg'),
        self.gui_config)    