import logging
from threading import Event, Thread
from .database import Database
from .gui_config import GuiConfiguration
from .scripts.json_config import load_json_config
from .templates import data_object_list, gui_configuration


logger = logging.getLogger('main_model')


class Model():
    def __init__(self) -> None:
        try:
            self.database = Database.init_dict(load_json_config('./data/data_object_list.json', data_object_list))  
            self.gui_configuration = GuiConfiguration.init_dict(load_json_config('./data/gui_configuration.json', gui_configuration))
        except Exception as error:
            logger.error(f'Could not load data_object_list.json due {error}')
            raise(error)
        self.event = Event()
        self.thread = None             
