import logging
import win32print
from model.gui_config import GuiConfiguration
from view.add_treeview import AddTreeview


logger = logging.getLogger('add_treeview_controller')


class AddTreeviewController:
    '''
    AddTreeviewController
    ---------------------

    Controller of AddTreeview GUI
    '''
    def __init__(self, add_treeview: AddTreeview, gui_configuration: GuiConfiguration) -> None:
        self.gui_configuration = gui_configuration
        self.frame = add_treeview
        self.last_grab = self.frame.grab_current()
        self.frame.grab_set()   
        win_pos = self.gui_configuration.check_update_win_pos(self.frame.geometry(), 'add_treeview')
        if win_pos:
            self.frame.geometry(win_pos)
        self.frame.protocol('WM_DELETE_WINDOW', self.destroy)  

        self.combobox_list = self.frame.combobox_list
        self.printer_name = ''

        self.button_ok = self.frame.button_ok
        self.button_cancel = self.frame.button_cancel
        
        self.printer_list = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)]
        self.printer_list.sort()
        self.combobox_list.config(values=self.printer_list)
        self.button_ok.config(command=self.ok_command)
        self.button_cancel.config(command=self.cancel_command)

    def ok_command(self, event=None) -> None:
        self.printer_name = self.combobox_list.get()
        self.destroy()

    def cancel_command(self, event=None) -> None:
        self.destroy()

    def get_printer(self) -> str:
        return self.printer_name

    def destroy(self) -> None:
        if self.last_grab:
            self.last_grab.grab_set()
        self.gui_configuration.check_update_win_pos(self.frame.geometry(), 'add_treeview')
        self.frame.destroy()