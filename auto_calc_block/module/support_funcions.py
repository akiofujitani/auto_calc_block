import logging
from . import json_config, file_handler
from .classes.config import Configuration, GuiConfiguration, TtkGeometry
from copy import deepcopy
from re import search

logger = logging.getLogger('suport_funcions')


def save_config_on_change(config: GuiConfiguration):
    r'''
    Save to configuration file if it has changes
    '''
    try:
        config_value = json_config.load_json_config('gui_config.json')
        old_config = GuiConfiguration.check_type_insertion(config_value)
        if not config.__eq__(old_config):
            temp_config = deepcopy(config)
            json_config.save_json_config('gui_config.json', temp_config.__dict__)
    except Exception as error:
        logger.error(f'Could not save configuration values {error}')  


# def update_count(config : ConfigurationValues) -> None:
#     r'''
#     Update files count in each directory in config object
#     '''
#     for path_value in config.path_list:
#         try:
#             file_list = file_handler.file_list(path_value.path, path_value.extension)
#             if path_value.ignore:
#                 for file_name in file_list:
#                     if reg_ex_ignore(path_value.ignore, file_name):
#                         file_list.remove(file_name)
#             logger.info(f'<PATH>path_name:{path_value.name},quantity:{len(file_list)}')
#         except Exception as error:
#             logger.error(f'Update count error {error}')
#     return


def reg_ex_ignore(reg_ex: str, search_value: str) -> bool:
    r'''
    Regex search returning boolean
    ----- ------ --------- -------
    
    The ignore must be in the regex format
    See Python RegEx Documentation

    '''
    if search(reg_ex, search_value):
        return True
    return False