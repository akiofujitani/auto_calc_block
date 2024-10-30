import logging
from tkinter import Toplevel, Label, Button, StringVar, Frame, Tk
from tkinter.ttk import Combobox


logger = logging.getLogger('add_treeview')


class AddTreeview(Toplevel):
    '''
    AddTreeview
    -----------

    Treeview add window
    '''
    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.master = master
        self.title('Add Printer')
        self.minsize(500, 150)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure([0, 1, 2], weight=1)

        Label(self, text='Please select the desired printer', justify='center').grid(column=0, row=0, columnspan=3, sticky='nesw', padx=5, pady=5)
        self.combobox_list = Combobox(self)
        self.combobox_list.grid(column=0, row=1, columnspan=3, sticky='nesw', padx=5, pady=5)
 
        frame_button = Frame(self)
        frame_button.grid(column=0, row=2, columnspan=3, sticky='nesw')
        frame_button.grid_columnconfigure(0, weight=1)
        frame_button.grid_rowconfigure(0, weight=1)
        self.button_ok = Button(frame_button, text='Ok', width=15)
        self.button_ok.grid(column=1, row=0, sticky='nesw', padx=5, pady=5)
        self.button_cancel = Button(frame_button, text='Cancel', width=15)
        self.button_cancel.grid(column=2, row=0, sticky='nesw', padx=5, pady=5)


if __name__ == '__main__':
    root = Tk()
    main_frame = Frame(root)
    main_frame.grid(column=0, row=0, sticky='nesw')
    settings = AddTreeview(main_frame)
    root.mainloop()
