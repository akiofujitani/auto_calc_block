import logging
from tkinter import Frame, Button, Label, Tk, Entry, WORD, Scrollbar
from tkinter.ttk import Treeview
from .img import Images

logger = logging.getLogger('nome')


class MainView(Frame):
    def __init__(self, master: Tk, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master      
        self.img = Images()
        self.master.wm_iconphoto(True, self.img.icon)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)        
        button_frame = Frame(self)
        button_frame.grid(column=0, row=0, columnspan=4, sticky='nesw')
        button_frame.grid_columnconfigure(0, weight=1)

        Label(button_frame, text='Insira o número do pedido para bloquear calculo automático:'  ).grid(column=0, row=0, columnspan=3, padx=5, pady=5, sticky='nesw')
        self.entry_job = Entry(button_frame, justify='center')
        self.entry_job.grid(column=0, row=1, padx=5, pady=5, sticky='nesw')
        button_dimension = 35
        self.button_send = Button(button_frame, text='Send', image=self.img.file, compound='left', width=100, height=button_dimension)
        self.button_send.grid(column=1, row=1, padx=(0, 5), pady=5, sticky='nesw')
        self.button_setting = Button(button_frame, text='Settings', image=self.img.settings, compound='left', width=100, height=button_dimension)
        self.button_setting.grid(column=2, row=1, padx=(0, 5), pady=5, sticky='nesw')

        treeview_frame = Frame(self)
        treeview_frame.grid(column=0, row=1, columnspan=4, sticky='nesw')
        treeview_frame.grid_columnconfigure(0, weight=1)
        treeview_frame.grid_rowconfigure(0, weight=1)

        self.columns = ('job_number', 'insertion_date')
        columns_description = ('Job Number', 'Insertion Date')
        columns_witdh = (120, 150)
        scrollbar = Scrollbar(treeview_frame, orient='vertical')
        self.treeview = Treeview(treeview_frame, columns=self.columns, show='headings', yscrollcommand=scrollbar.set)
        self.treeview.grid(column=0, row=0, columnspan=3, sticky='nesw', padx=(5, 0), pady=5)
        scrollbar.grid(column=3, row=0, sticky='nesw', padx=(0, 5), pady=5)
        scrollbar.config(command=self.treeview.yview)
        self.treeview.tag_configure('evenrow', background='white')
        self.treeview.tag_configure('oddrow', background='#E0E0E0')
        for i, column in enumerate(self.columns):
            self.treeview.heading(column, text=columns_description[i])
            self.treeview.column(column, width=columns_witdh[i], anchor='center')

