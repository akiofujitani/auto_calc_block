from os.path import normpath, abspath
from datetime import time

class Configuration:
    '''
    Configuration
    -------------
    
    Args
        - source_path
        - destin_path
        - print_program
        - print_command
        - extension
        - printer_list
        - wait_time
        - print_interval
        - start_delay
        - start_min
        - print_start_time
        - print_end_time
        
    Methods
        - init_dict (classmethod)

    '''    
    def __init__(self, source_path: str, destin_path: str, print_program: str, print_command: str, extension : str, printer_list: list[str], wait_time: int, print_interval: int, start_delay: int, start_min: bool, print_start_time: time, print_end_time: time) -> None:
        self.source_path = source_path
        self.destin_path = destin_path
        self.print_program = print_program
        self.print_command = print_command
        self.extension = extension
        self.printer_list = printer_list
        self.wait_time = wait_time
        self.print_interval = print_interval
        self.start_delay = start_delay
        self.start_min = start_min
        self.print_start_time = print_start_time
        self.print_end_time = print_end_time

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True

    def add_printer(self, printer_name: str) -> bool:
        if not printer_name in self.printer_list:
            self.printer_list.append(printer_name)
            self.printer_list.sort()
            return True
        return False

    def remove_printer(self, printer_name: str) -> bool:
        if printer_name in self.printer_list:
            self.printer_list.remove(printer_name)
            return True
        return False

    @classmethod
    def init_dict(cls, setting_dict=dict):
        source_path = abspath(normpath(setting_dict.get('source_path')))
        destin_path = abspath(normpath(setting_dict.get('destin_path')))
        print_program = abspath(normpath(setting_dict.get('print_program')))
        print_command = setting_dict.get('print_command')
        extension = setting_dict.get('extension')
        printer_list = [printer for printer in setting_dict.get('printer_list')]
        wait_time = int(setting_dict.get('wait_time'))
        print_interval = int(setting_dict.get('print_interval'))
        start_delay = int(setting_dict.get('start_delay'))
        start_min = eval(setting_dict.get('start_min'))
        print_start_time = time(*[int(num) for num in setting_dict.get('print_start_time').split(':')])
        print_end_time = time(*[int(num) for num in setting_dict.get('print_end_time').split(':')])
        return cls(source_path, destin_path, print_program, print_command, extension, printer_list, wait_time, print_interval, start_delay, start_min, print_start_time, print_end_time)