from tkinter import Toplevel, Label, Entry, Scrollbar, Frame, Button, Checkbutton, Tk
from tkinter.scrolledtext import ScrolledText
from tkinter.ttk import Treeview

class Settings(Toplevel):
    '''
    Settings
    --------

    Settings window
    '''
    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.master = master
        self.title('Settings')
        self.minsize(500, 620)

        row_num = 0

        Label(self, text='Source File Path', justify='right').grid(column=0, row=row_num, sticky='nesw', padx=5, pady=5)
        self.entry_source_path = Entry(self, width=20, justify='center')
        self.entry_source_path.grid(column=1, row=row_num, columnspan=3, sticky='news', padx=(5, 0), pady=5)
        row_num += 1
        Label(self, text='Destin File Name', justify='right').grid(column=0, row=row_num, sticky='nesw', padx=5, pady=5)
        self.entry_destin_path = Entry(self, width=20, justify='center')
        self.entry_destin_path.grid(column=1, row=row_num, columnspan=3, sticky='nesw', padx=(5, 0), pady=5)
        row_num += 1
        Label(self, text='Print Program', justify='right').grid(column=0, row=row_num, sticky='nesw', padx=5, pady=5)
        self.entry_program_path = Entry(self, width=20, justify='center')
        self.entry_program_path.grid(column=1, row=row_num, columnspan=3, sticky='news', padx=(5, 0), pady=5)            
        row_num += 1
        Label(self, text='Print Command', justify='right').grid(column=0, row=row_num, sticky='nesw', padx=5, pady=5)
        self.scrl_text_print_command = ScrolledText(self, width=20, height=7)
        self.scrl_text_print_command.grid(column=1, row=row_num, columnspan=4, sticky='nesw', padx=5, pady=5)  
        row_num += 1
        Label(self, text='Extension', justify='right').grid(column=0, row=row_num, sticky='nesw', padx=5, pady=5)
        self.entry_extension = Entry(self, width=20, justify='center')
        self.entry_extension.grid(column=1, row=row_num, sticky='news', padx=5, pady=5)
        Label(self, text='Wait Time', justify='right').grid(column=2, row=row_num, sticky='nesw', padx=5, pady=5)
        self.entry_wait_time = Entry(self, width=20, justify='center')
        self.entry_wait_time.grid(column=3, row=row_num, columnspan=2, sticky='news', padx=5, pady=5)
        row_num += 1
        Label(self, text='Print Interval', justify='right').grid(column=0, row=row_num, sticky='nesw', padx=5, pady=5)
        self.entry_print_interval = Entry(self, width=20 , justify='center')
        self.entry_print_interval.grid(column=1, row=row_num, sticky='news', padx=5, pady=5)
        Label(self, text='Start Delay', justify='right').grid(column=2, row=row_num, sticky='nesw', padx=5, pady=5)        
        self.entry_start_delay = Entry(self, width=20, justify='center')
        self.entry_start_delay.grid(column=3, row=row_num, columnspan=2, sticky='news', padx=5, pady=5)
        row_num += 1
        Label(self, text='Print Time', justify='right').grid(column=0, row=row_num, sticky='nesw', padx=5, pady=5)
        self.entry_print_start_time = Entry(self, width=10, justify='center')
        self.entry_print_start_time.grid(column=1, row=row_num, sticky='news', padx=5, pady=5)
        Label(self, text='until', justify='right').grid(column=2, row=row_num, sticky='nesw', padx=5, pady=5)
        self.entry_print_end_time = Entry(self, width=10, justify='center')
        self.entry_print_end_time.grid(column=3, columnspan=2, row=row_num, sticky='news', padx=5, pady=5)
        row_num += 1
        Label(self, text='Start minimized', justify='right').grid(column=0, row=row_num, sticky='nesw', padx=5, pady=5)
        self.check_start_min = Checkbutton(self, justify='center')
        self.check_start_min.grid(column=1, row=row_num, columnspan=4, sticky='nesw', padx=5, pady=5)
        row_num += 1             
        Label(self, text='Printer List', justify='right').grid(column=0, row=row_num, sticky='nesw', padx=5, pady=5)

        treeview_frame = Frame(self)
        treeview_frame.grid(column=1, row=row_num, columnspan=4, rowspan=2, sticky='nesw')
        row_num += 1
        treeview_frame.grid_columnconfigure([1, 2, 3], weight=1)

        self.columns = ('index', 'printer')
        columns_description = ('Index', 'Printer')
        columns_width = (25, 100)
        anchor_value = ('center', 'w')
        scrollbar = Scrollbar(treeview_frame, orient='vertical', background='white')
        self.treeview = Treeview(treeview_frame, columns=self.columns, height=5, show='headings', yscrollcommand=scrollbar.set)
        self.treeview.grid(column=1, row=0, columnspan=3, sticky='nesw', padx=(5, 0), pady=(0, 5))
        scrollbar.grid(column=4, row=0, sticky='nesw', padx=(0, 3), pady=(0, 5))
        scrollbar.config(command=self.treeview.yview)
        self.treeview.tag_configure('evenrow', background='white')
        self.treeview.tag_configure('oddrow', background='#E0E0E0')

        self.button_add = Button(treeview_frame, text='Add')
        self.button_add.grid(column=2, row=1, sticky='nesw', padx=(5, 0), pady=(0, 5))
        self.button_remove = Button(treeview_frame, text='Remove', width=5)
        self.button_remove.grid(column=3, row=1, columnspan=2, sticky='nesw', padx=(0, 5), pady=(0, 5))

        for i, column in enumerate(self.columns):
            self.treeview.heading(column, text=columns_description[i])
            self.treeview.column(column, width=columns_width[i], anchor=anchor_value[i])           

        self.button_source_path = Button(self, text='...', width=5)
        self.button_source_path.grid(column=4, row=0, sticky='nesw', padx=(0, 5), pady=5)
        self.button_destin_path = Button(self, text='...', width=5)
        self.button_destin_path.grid(column=4, row=1, sticky='nesw', padx=(0, 5), pady=5)
        self.button_program_path = Button(self, text='...', width=5)
        self.button_program_path.grid(column=4, row=2, sticky='nesw', padx=(0, 5), pady=5)                

        row_num += 1
        button_frame = Frame(self)
        button_frame.grid(column=0, row=row_num, columnspan=5, sticky='nesw')
        button_frame.grid_rowconfigure(0, minsize=40)
        button_frame.grid_columnconfigure(0, weight=1)

        for i in range(row_num + 1):
            self.grid_rowconfigure(i, weight=1, minsize=40)
        self.grid_columnconfigure([1, 3], weight=1)

        self.button_cancel = Button(button_frame, text='Cancel', width=15)
        self.button_ok = Button(button_frame, text='Ok', width=15)
        self.button_cancel.grid(column=1, row=0, sticky='nesw', padx=(5, 0), pady=5)
        self.button_ok.grid(column=2, row=0, sticky='nesw', padx=5, pady=5)


if __name__ == '__main__':
    root = Tk()
    main_frame = Frame(root)
    main_frame.grid(column=0, row=0, sticky='nesw')
    settings = Settings(main_frame)
    root.mainloop()
