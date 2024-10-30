import logging
from tkinter import Menu, Frame, Toplevel, Tk, END
from tkinter.messagebox import askokcancel
from queue import Queue
from pystray import MenuItem, Icon
from view.main_view import MainView
from view.about import About
from view.settings import Settings
from controller.about_controller import AboutController
from controller.settings_controller import SettingsController
from model.main import Model
from model.scripts.file_handler import resource_path

logger = logging.getLogger('main_view_controller')


class MainViewController:
    """
    MainViewController
    ------------------

    Attributes
        - main: MainView
        - model: Model
        - log_queue: Queue    
    """

    def __init__(self, main: MainView, model: Model, log_queue: Queue) -> None:
        self.main = main
        self.model = model
        self.master = main.master
        self.gui_configuration = self.model.gui_configuration
        self.configuration = self.model.database.get('config')
        self.log_queue = log_queue
        self.console_logging = ConsoleLogging(log_queue, self.main, self.master)
        self.tray_menu = (MenuItem('Restore', self.__show_window), MenuItem('Quit', self.__quit))

        menu_bar = Menu(self.main)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Start   ', command=self.__start)
        file_menu.add_command(label='Stop    ', command=self.__stop)        
        file_menu.add_separator()
        file_menu.add_command(label='Exit   ', command=self.__quit)

        settings_menu = Menu(menu_bar, tearoff=0)
        settings_menu.add_command(label='Settings  ', command=self.__settings)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label='About   ', command=self.__about)
        menu_bar.add_cascade(label='File   ', menu=file_menu)
        menu_bar.add_cascade(label='Settings   ', menu=settings_menu)    
        menu_bar.add_cascade(label='Help   ', menu=help_menu)

        self.master.config(menu=menu_bar)
        self.master.protocol('WM_DELETE_WINDOW', self.__hide_window_to_tray)
        # self.master.after(100, self.__pull_log)  
        self.main.start_button.config(command=self.__start)
        self.main.stop_button.config(command=self.__stop)
        self.main.config_button.config(command=self.__settings)

        if self.configuration.start_min:
            self.__hide_window_to_tray()

    def __start(self):
        logger.debug('Start')
        self.model.start_routine()

    def __stop(self):
        logger.debug('Stop')
        self.model.stop_routine()

    def __settings(self):
        '''
        Settings
        --------

        Open settings window
        '''
        self.model.stop_routine()
        self.settings = Settings(self.master)
        self.settings_controller = SettingsController(self.settings, self.model.database, self.gui_configuration)
        logger.debug('Settings')

    def __quit(self):
        if askokcancel('Quit', 'Do you want to quit?'):
            self.gui_configuration.check_update_win_pos(self.master.geometry(), 'main')
            self.model.on_close() 
            try:
                self.tray_icon.stop()
            except:
                logger.warning('Application in normal mode')
            logger.info('Forcing kill thread if it is open')                
            self.master.after(0, self.master.deiconify)      
            self.master.destroy()

    def __about(self):
        logger.info('About clicked')
        about = About('''
            Application name: Print Manager
            Version: 1.00.00
            Developed by: Akio Fujitani
            e-mail: akiofujitani@gmail.com
        ''', resource_path('./Img/bedo_mora_siris.png'))
        self.about_controller = AboutController(self.master, about, self.gui_configuration)

    def __show_window(self) -> None:
        self.tray_icon.stop()
        self.master.after(50, self.master.deiconify)

    def __hide_window_to_tray(self) -> None:
        self.__start()
        window_close_list = []
        for children in self.master.children:
            if isinstance(self.master.children[children], Toplevel):
                window_close_list.append(children)
        for children in window_close_list:
            self.master.children[children].destroy()
        logger.debug('Run tray icon')
        self.master.withdraw()

        self.tray_icon = Icon('Tkinter GUI', self.main.icon, 
                              'Print Manager', self.tray_menu)
        self.tray_icon.run()

class ConsoleLogging:
    '''
    ConsoleLogging
    --------------

    Class for logging display.

    Attributes
        - log_queue
        - main_frame
        - master
    
    '''
    def __init__(self, log_queue: Queue, main_frame: Frame, master: Tk) -> None:
        self.main = main_frame
        self.master = master
        self.log_queue = log_queue
        self.master.after(100, self.__pull_log)  

    def __pull_log(self) -> None:
        message = ''
        while not self.log_queue.empty():
            message += f'{self.log_queue.get(block=False)}\n' 
        if message:
            self.__display(message)
        self.master.after(100, self.__pull_log)

    def __display(self, message) -> None:
        self.main.scrolled_text.configure(state='normal')
        line_count = int(float(self.main.scrolled_text.index('end')))
        if line_count > 500:
            self.main.scrolled_text.delete('1.0', str("{:0.1f}".format(line_count - 499)))
        self.main.scrolled_text.insert(END, f'{message}')
        self.main.scrolled_text.configure(state='disabled')
        self.main.scrolled_text.yview(END)