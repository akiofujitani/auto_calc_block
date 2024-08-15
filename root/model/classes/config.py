from os.path import normpath


class Configuration:
    r'''
    Configuration
    -------------
    
    Args
        - file_path
        - file_name
        - file_extension
        - job_minimum_length
        - days_to_keep

        
    Methods
        - init_dict (classmethod)

    '''
    def __init__(self, file_path: str, file_name: str, file_extension: str, job_minimum_length: int, days_to_keep: int) -> None:
        self.file_path = file_path
        self.file_name = file_name
        self.file_extension = file_extension
        self.job_minimum_length = job_minimum_length
        self.days_to_keep = days_to_keep

    def __eq__(self, __o: object) -> bool:
        if not isinstance(__o, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(__o, key):
                    return False
            return True

    @classmethod
    def init_dict(cls, dict_values: dict[str, str]) -> object:
        file_path =  normpath(dict_values.get('file_path'))
        file_name = str(dict_values.get('file_name'))
        file_extension = str(dict_values.get('file_extension'))
        job_minimum_length = int(dict_values.get('job_minimum_length'))
        days_to_keep = int(dict_values.get('days_to_keep'))
        return cls(file_path, file_name, file_extension, job_minimum_length, days_to_keep)