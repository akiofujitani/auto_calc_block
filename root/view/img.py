import logging
from tkinter import Tk, Frame
from os.path import normpath
from model.scripts.file_handler import resource_path
from model.constants import IMG_PATH
from PIL import Image, ImageTk

logger = logging.getLogger('img')


class Images(Frame):
    def __init__(self, *args, **kwargs) -> None:
        '''
        https://www.flaticon.com/free-icons/send
        https://www.flaticon.com/free-icons/settings

        https://www.flaticon.com/free-icons/black-cat
        '''
        try:
            image_dimension = 35
            file_image = Image.open(resource_path(normpath(IMG_PATH + '/file.png')))
            file_image.thumbnail((image_dimension, image_dimension), Image.Resampling.LANCZOS)
            settings_image = Image.open(resource_path(normpath(IMG_PATH + '/setting.png')))
            settings_image.thumbnail((image_dimension, image_dimension), Image.Resampling.LANCZOS)            
            icon_path = resource_path(normpath(IMG_PATH + '/black-cat.png'))
            icon_image = Image.open(icon_path)
            icon_image.thumbnail((96, 96), Image.Resampling.LANCZOS)            
            
            self.icon = ImageTk.PhotoImage(icon_image)            
            self.file = ImageTk.PhotoImage(file_image)
            self.settings = ImageTk.PhotoImage(settings_image)
        except Exception as error:
            logger.error(f'Could not load icon {error}')