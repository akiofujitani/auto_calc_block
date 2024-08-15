import logging
from queue import Queue
from threading import Event, Thread
from tkinter import messagebox
from tkinter import ttk
from module import json_config, log_builder
from module.classes.config import Configuration, GuiConfiguration, config_template, gui_config_template
from module.gui import MainApp

logger = logging.getLogger('auto_calc_block')


def main(event: Event, config: Configuration):
    pass


if __name__ == '__main__':
    log_queue = Queue()
    logger = logging.getLogger()
    log_builder.logger_setup(logger, log_queue)

    event = Event()

    try:
        config_values = json_config.load_json_config('config.json', config_template)
        config = Configuration.init_dict(config_values)
        gui_config_values = json_config.load_json_config('gui_config.json', gui_config_template)
        gui_config = GuiConfiguration.init_dict(gui_config_values)
    except Exception as error:
        logger.critical(f'Configuration error {error}')
        exit()
    

    logger.debug('test')
    main_thread = Thread(target=main, args=(event, config, ), daemon=True, name='auto_calc_block')
    main_thread.start()

    main_app = MainApp('Auto Calculation', log_queue, config, gui_config)
    main_app.mainloop() 