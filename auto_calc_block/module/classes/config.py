import logging
from os.path import normpath
from dataclasses import dataclass
from collections import namedtuple

logger = logging.getLogger('config')


config_template = '''
{
    "block_file_path" : ".",
    "block_file" : "auto_calc_block.txt"
}
'''


gui_config_template = '''
{
    "update_time" : "10",
    "list_geometry" : {
        "main" : [
            "", 
            "", 
            0, 
            0
        ],
        "settings" : [
            "", 
            "", 
            0, 
            0
        ],
        "edit" : [
            "", 
            "", 
            0, 
            0
        ],
        "list_view" : [
            "", 
            "", 
            0, 
            0
        ]
    },
    "always_on_top" : "False",
    "path_list" : [
        {
            "name" : "Template",
            "path" : "./",
            "extension" : "",
            "ignore" : ""
        }
    ]
}
'''

TtkGeometry = namedtuple('TtkGeometry', 'width height x y')


@dataclass
class Configuration:
    r'''
    Configuration
    -------------

    Configuration values
    '''
    block_file_path : str
    block_file : str

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True
    
    @property
    def to_dict(self):
        dict_config = {}
        dict_config['block_file_path'] = self.block_file_path
        dict_config['block_file'] = self.block_file
        return dict_config

    @classmethod
    def init_dict(cls, config_values: dict):
        try:
            block_file_path = normpath(config_values.get('block_file_path'))
            block_file = config_values.get('block_file')
            return cls(block_file_path, block_file)
        except Exception as error:
            raise error


@dataclass
class GuiConfiguration:
    list_geometry : dict

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True
    
    @property
    def to_dict(self):
        dict_config = {}
        dict_config['list_geometry'] = {gui_name : [gui_value.width, gui_value.height, gui_value.x, gui_value.y] for gui_name, gui_value in self.list_geometry.items()}
        return dict_config

    def update_win_size_pos(self, geometry_str:str, window_name: str) -> None:
        r'''
        Update window size and position in config object
        '''
        temp_splited_geometry = geometry_str.split('+')
        win_size = temp_splited_geometry[0].split('x')
        win_pos = [temp_splited_geometry[1], temp_splited_geometry[2]]
        main_pos = self.list_geometry.get(window_name)
        if not win_size[0] == main_pos.width or not win_size[1] == main_pos.height or not win_pos[0] == main_pos.x or not win_pos[1] == main_pos.y:
            logger.debug(f'{win_size[0]} x {win_size[1]} + {win_pos[0]} + {win_pos[1]}')
            main_pos = TtkGeometry(win_size[0], win_size[1], win_pos[0], win_pos[1])
            self.list_geometry[window_name] = main_pos
        return

    def check_win_pos(self, win_name: str) -> str:
        r'''
        Get win position in configuration object
        '''
        try:
            config_win_pos = self.list_geometry.get(win_name)
            if config_win_pos.width and config_win_pos.height:
                geometry_values = f'{config_win_pos.width}x{config_win_pos.height}+{config_win_pos.x}+{config_win_pos.y}'
                logger.debug(geometry_values)
                return geometry_values
        except Exception as error:
            logger.error(f'Error getting window position due {error}')
            raise error

    @classmethod
    def init_dict(cls, config_values: dict):
        try:
            list_geometry = {name : TtkGeometry(*value) for name, value in config_values.get('list_geometry').items()}
            return cls(list_geometry)
        except Exception as error:
            raise error

@dataclass
class LanguageSettings:
    title : str
    insert_job: str
    insert_job_button: str
    not_found_message: str