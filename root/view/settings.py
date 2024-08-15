from tkinter import Toplevel, Label, Entry, Frame, Button


class Setting(Toplevel):
    def __init__(self, master, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.master = master
        self.title('Settings')
        self.minsize(500, 250)
        for i in range(6):
            self.grid_rowconfigure(i, weight=1, minsize=40)
        self.grid_columnconfigure(1, weight=1)

        Label(self, text='Block File Path', justify='right').grid(column=0, row=0, sticky='nesw', padx=5, pady=5)
        Label(self, text='Block File Name', justify='right').grid(column=0, row=1, sticky='nesw', padx=5, pady=5)
        Label(self, text='Block File Extension', justify='right').grid(column=0, row=2, sticky='nesw', padx=5, pady=5)
        Label(self, text='Job Minimum Length', justify='right').grid(column=0, row=3, sticky='nesw', padx=5, pady=5)
        Label(self, text='Store time', justify='right').grid(column=0, row=4, sticky='nesw', padx=5, pady=5)

        self.entry_file_path = Entry(self, width=20)
        self.entry_file_name = Entry(self, width=20, justify='center')
        self.entry_file_extension = Entry(self, width=20, justify='center')
        self.entry_job_minimum_lenght = Entry(self, width=20, justify='center')
        self.entry_store_time = Entry(self, width=20, justify='center')
        self.entry_file_path.grid(column=1, row=0, sticky='news', padx=(5, 0), pady=5)
        self.entry_file_name.grid(column=1, row=1, columnspan=2, sticky='nesw', padx=5, pady=5)
        self.entry_file_extension.grid(column=1, row=2, columnspan=2, sticky='news', padx=5, pady=5)
        self.entry_job_minimum_lenght.grid(column=1, row=3, columnspan=2, sticky='nesw', padx=5, pady=5)
        self.entry_store_time.grid(column=1, row=4, columnspan=2, sticky='news', padx=5, pady=5)

        self.button_file_path = Button(self, text='...', width=5)
        self.button_file_path.grid(column=2, row=0, sticky='nesw', padx=(0, 5), pady=5)

        button_frame = Frame(self)
        button_frame.grid(column=0, row=5, columnspan=3, sticky='nesw')
        button_frame.grid_rowconfigure(0, minsize=40)
        button_frame.grid_columnconfigure(0, weight=1)

        self.button_cancel = Button(button_frame, text='Cancel', width=15)
        self.button_ok = Button(button_frame, text='Ok', width=15)
        self.button_cancel.grid(column=1, row=0, sticky='nesw', padx=(5, 0), pady=5)
        self.button_ok.grid(column=2, row=0, sticky='nesw', padx=5, pady=5)
