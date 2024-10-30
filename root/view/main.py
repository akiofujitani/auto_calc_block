from .root import Root
from .main_view import MainView


class View:
    '''
    Base class for GUI
    '''
    def __init__(self) -> None:
        self.root = Root()
        self.root.title('Printer Manager')
        self.main_view = MainView(self.root)
        self.main_view.grid(column=0, row=0, sticky='nesw')

    def start_main_loop(self):
        self.root.mainloop()