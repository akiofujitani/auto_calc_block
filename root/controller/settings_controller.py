import logging
from copy import deepcopy
from os.path import normpath, exists, isfile, dirname
from os import mkdir
from datetime import time
from tkinter import Entry, IntVar
from tkinter.filedialog import askdirectory, askopenfilename
from tkinter.messagebox import askquestion, showerror
from model.database import Database
from model.classes.config import Configuration
from model.scripts.file_handler import resource_path
from model.gui_config import GuiConfiguration
from view.settings import Settings
from view.add_treeview import AddTreeview
from controller.add_treeview_controller import AddTreeviewController
from controller.validation_controller import int_validate

logger = logging.getLogger('settings_controller')


class SettingsController:
    '''
    SettingsController
    ------------------

    attributes
        - settings_view (Settings)
        - database (Database)
        - gui_configuration (GuiConfiguration)
    '''
    def __init__(self, settings_view: Settings, database: Database, gui_configuration: GuiConfiguration) -> None:
        self.frame = settings_view
        self.database = database
        self.gui_configuration = gui_configuration
        self.configuration = deepcopy(self.database.get('config'))
        self.last_grab = self.frame.grab_current()
        self.frame.grab_set()   
        win_pos = self.gui_configuration.check_update_win_pos(self.frame.geometry(), 'settings')
        if win_pos:
            self.frame.geometry(win_pos)
        self.frame.protocol('WM_DELETE_WINDOW', self.__on_window_close)  

        # Widgets Entries
        self.entry_source_path = self.frame.entry_source_path
        self.entry_destin_path = self.frame.entry_destin_path
        self.entry_program_path = self.frame.entry_program_path
        self.entry_extension = self.frame.entry_extension
        self.entry_wait_time = self.frame.entry_wait_time
        self.entry_print_interval = self.frame.entry_print_interval
        self.entry_start_delay = self.frame.entry_start_delay
        self.entry_print_start_time = self.frame.entry_print_start_time
        self.entry_print_end_time = self.frame.entry_print_end_time

        self.scrl_text_print_command = self.frame.scrl_text_print_command

        self.bool_check = IntVar(self.frame.master)
        self.check_start_min = self.frame.check_start_min
        self.check_start_min.config(variable=self.bool_check)

        self.treeview = self.frame.treeview
        self.button_add = self.frame.button_add
        self.button_remove = self.frame.button_remove

        # Widgets Buttons
        self.button_source_path = self.frame.button_source_path
        self.button_destin_path = self.frame.button_destin_path
        self.button_program_path = self.frame.button_program_path
        self.button_cancel = self.frame.button_cancel
        self.button_ok = self.frame.button_ok

        # Commands
        self.button_source_path.config(command=lambda arg=self.entry_source_path: self.file_path_command(arg))
        self.button_destin_path.config(command=lambda arg=self.entry_destin_path: self.file_path_command(arg))
        self.button_program_path.config(command=lambda arg=self.entry_program_path, is_file=True: self.file_path_command(arg, is_file))
        self.button_add.config(command=self.treeview_add_command)
        self.button_remove.config(command=self.treeview_remove_command)
        self.button_cancel.config(command=self.cancel_command)
        self.button_ok.config(command=self.ok_command)
        self.entry_path_list = [self.entry_source_path, self.entry_destin_path, self.entry_program_path]
        self.entry_str_list = [self.entry_extension]
        self.entry_int_list = [self.entry_wait_time, self.entry_print_interval, self.entry_start_delay]
        self.entry_time_list = [self.entry_print_start_time, self.entry_print_end_time]
        self.fill_entries()

        # Validation
        self.int_vcmd = (self.frame.register(int_validate), 
                        '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')

        for column in self.frame.columns:
            self.treeview.heading(column, command=lambda column_value=column: self.__sort_tree_view(column_value, False))

    def __sort_tree_view(self, colum_value, descending):
        '''
        __sort_tree_view
        ----------------

        Sort treeview by selected column

        https://www.w3resource.com/python-exercises/tkinter/python-tkinter-widgets-exercise-18.php
        '''
        tree_view_data = [(self.tree_view.set(item, colum_value), item) for item in self.tree_view.get_children('')]
        tree_view_data.sort(reverse=descending)
        even_odd = {0 : 'evenrow', 1 : 'oddrow'}
        for index, (_, item) in enumerate(tree_view_data):
            self.treeview.move(item, '', index)
            self.treeview.item(item, tags=(even_odd.get(index % 2)))
        self.tree_view.heading(colum_value, command=lambda: self.__sort_tree_view(colum_value, not descending))

    def set_treeview(self, values_list: list[str]) -> None:
        '''
        Set values on treeview GUI
        '''
        even_odd = {0: 'evenrow', 1: 'oddrow'}
        self.treeview.delete(*self.treeview.get_children())
        if len(values_list) > 0:
            for i, value in enumerate(values_list):
                self.treeview.insert('', 'end', values=(i, value), tags=(even_odd.get(i % 2)))

    def file_path_command(self, entry_widget: Entry, is_file: bool=False, event=None) -> None:
        if is_file:
            file_path = askopenfilename(initialdir='/', title='Select file')
        else:
            file_path = askdirectory(initialdir='/', title='Select path')
        old_path = entry_widget.get()
        if file_path:
            try:
                file_path = normpath(file_path)
                entry_widget.delete(0, 'end')
                entry_widget.insert('end', str(file_path))
                entry_widget.lift()
                logger.debug(f'File path {file_path}')
            except Exception as error:
                logger.warning(f'Could not get file path due {error}')
                if old_path:
                    entry_widget.delete(0, 'end')
                    entry_widget.insert('end', str(old_path))

    def treeview_add_command(self, event=None) -> None:
        '''
        Treeview Add Command
        --------------------

        add printer to treeview
        '''
        self.treeview_add = AddTreeview(self.frame.master)
        self.treeview_add_controller = AddTreeviewController(self.treeview_add, self.gui_configuration)
        self.frame.wait_window(self.treeview_add)
        printer_name = self.treeview_add_controller.get_printer()
        self.configuration.add_printer(printer_name)
        self.clear()
        self.fill_entries()

    def treeview_remove_command(self, event=None) -> None:
        '''
        Treeview Remove Command
        -----------------------
        '''
        printer_name = self.treeview.item(self.treeview.selection()[0]).get('values')[1]
        self.configuration.remove_printer(printer_name)
        self.clear()
        self.fill_entries()      

    def cancel_command(self, event=None) -> None:
        self.save_close()

    def ok_command(self, event=None) -> None:
        self.save_close()

    def save_close(self) -> None:
        '''
        Save Close
        ----------

        Compare values in the settings GUI with the saved values and confirms save
        '''
        old_config = self.database.get('config')
        if not old_config.__eq__(self.configuration):
            answer = askquestion('Configuration save', 'Changes were made in configuration. \nDo you want to save it?')
            if answer == 'yes':
                self.save(self.configuration)
        self.destroy()

    def save(self, new_config: Configuration) -> None:
        try:
            self.database.save_update('config', new_config)
        except Exception as error:
            logger.error(f'Could not save due {error}')
            showerror('Save error', f'Could not save configuration due {error}')
        finally:
            return

    def fill_entries(self) -> None:
        '''
        Fill all values from configuration in GUI 
        '''
        self.clear()
        self.entry_source_path.insert(0, self.configuration.source_path)
        self.entry_destin_path.insert(0, self.configuration.destin_path)
        self.entry_program_path.insert(0, self.configuration.print_program)
        self.entry_extension.insert(0, self.configuration.extension)
        self.entry_wait_time.insert(0, self.configuration.wait_time)
        self.entry_print_interval.insert(0, self.configuration.print_interval)
        self.entry_start_delay.insert(0, self.configuration.start_delay)
        self.entry_print_start_time.insert(0, self.configuration.print_start_time)
        self.entry_print_end_time.insert(0, self.configuration.print_end_time)
        self.scrl_text_print_command.insert('end', self.configuration.print_command.rstrip())
        self.bool_check.set(self.configuration.start_min)
        self.set_treeview(self.configuration.printer_list) 

    def check_format_path(self, path: str) -> str:
        '''
        Check path
        '''
        path = normpath(resource_path(path))
        if isfile(path):
            path_dir = dirname(path)
        else:
            path_dir = path
        if not exists(path_dir):
            mkdir(path_dir)
        return path

    # def get_entries(self) -> Configuration:
    #     try:
    #         new_source_path = self.check_format_path(self.entry_source_path.get())
    #         new_destin_path = self.check_format_path(self.entry_destin_path.get())
    #         new_program_path = self.check_format_path(self.entry_program_path.get())
    #         new_extension = str(self.entry_extension.get())
    #         new_wait_time = int(self.entry_wait_time.get())
    #         new_print_interval = int(self.entry_print_interval.get())
    #         new_start_delay = int(self.entry_start_delay.get())
    #         new_print_start_time = time(*[int(value) for value in self.entry_print_start_time.get().split(':')] )
    #         new_print_end_time = time(*[int(value) for value in self.entry_print_end_time.get().split(':')])
    #         new_print_command = self.scrl_text_print_command.get("1.0", 'end')
    #         new_printer_list = [self.treeview.item(id).get('values')[1] for id in self.treeview.get_children()]
    #         new_start_min = self.bool_check.get()
    #         return Configuration(new_source_path, new_destin_path, new_program_path, new_print_command, new_extension, new_printer_list, 
    #                              new_wait_time, new_print_interval, new_start_delay, new_start_min, new_print_start_time, new_print_end_time)
    #     except Exception as error:
    #         showerror('Configuration error', 'Could not get configuration values.')
    #         logger.warning(f'Could not get entries due {error}')
    #         self.fill_entries()

    def clear(self) -> None:
        '''
        Clear
        -----

        Remove all values from the GUI
        '''
        for entry in self.entry_path_list + self.entry_str_list + self.entry_int_list + self.entry_time_list:
            entry.delete(0, 'end')
        self.scrl_text_print_command.delete('1.0', 'end')
        self.bool_check.set('')
        self.treeview.delete(*self.treeview.get_children())

    def __on_window_close(self):
        self.destroy()

    def destroy(self) -> None:
        if self.last_grab:
            self.last_grab.grab_set()
        self.gui_configuration.check_update_win_pos(self.frame.geometry(), 'settings')
        self.frame.destroy()