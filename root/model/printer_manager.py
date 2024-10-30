import win32print, logging, subprocess
from threading import Event
from os.path import join
from time import sleep
from datetime import time, datetime
from model.scripts import file_handler
from .database import Database
from .classes.config import Configuration


logger = logging.getLogger('print_manager')


def check_printers(printer_list_set: list) -> bool:
    '''
    Check printer in list
    '''
    printer_list_pc = [printer[2] for printer in win32print.EnumPrinters(win32print.PRINTER_ENUM_LOCAL, None, 1)]  # get printers
    compared_list = []
    for printer in printer_list_pc:
        if printer in printer_list_set:
            compared_list.append(printer)
    if len(compared_list) == len(printer_list_set):
        logger.debug('True')
        return True
    logger.debug('False')
    return False
    

def print_file(printer: str, print_program: str, print_command: str, file: str) -> None:
    '''
    Sent file to specific printer with command using cmd
    '''
    try:
        cmd = f'"{print_program}" {print_command} "{file}" "{printer}"'
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)    
        logger.info(f'Print message {proc}')
        return
    except Exception as error:
        logger.error(error)
        raise(error)


def get_jobs_in_printers(printer_list: list) -> dict:
    '''
    Get print jobs being printed in each printer in printer list
    '''
    printer_and_jobs = {}
    try:
        for printer in printer_list:
            printer_values = win32print.GetPrinter(win32print.OpenPrinter(printer), 2)
            printer_and_jobs[printer] = printer_values['cJobs']
            logger.debug(f'Printer {printer} : {printer_values["cJobs"]}')
        return printer_and_jobs
    except Exception as error:
        logger.error(f'Get jobs {error}')
        raise error


def check_print_time(start_print_time: time, end_print_time: time) -> bool:
    '''
    Check active print time
    '''
    now = datetime.now().time()
    if now >= start_print_time and now <= end_print_time:
        return True
    return False


def print_manager_main(event: Event, config: Configuration) -> None:
    '''
    Loads and execute distribution of files to printers in list
    This function runs indefinetely until an gui event is catch
    '''
    if check_printers(config.printer_list):
        print_program = config.print_program
        last_used_printer = ''
        last_job_in_printers = {}
        fail_list = []
        while True:
            if check_print_time(config.print_start_time, config.print_end_time):
                if event.is_set():
                    logger.info('Terminanting Print Manager')
                    return
                try:
                    file_list = file_handler.file_list(config.source_path, config.extension)
                    if len(fail_list) > 0:
                        file_list = file_list + fail_list
                        fail_list = []
                    if file_list:
                        for file in file_list:
                            if event.is_set():
                                logger.info('Terminanting Print Manager')
                                return
                            job_in_printers = get_jobs_in_printers(config.printer_list)
                            try:
                                if len(config.printer_list) == 1:
                                    print_file(config.printer_list[0], print_program, config.print_command, join(config.source_path, file))
                                    logger.info(f'File {file} sent to printer {config.printer_list[0]}')
                                else:
                                    for printer in config.printer_list:
                                        logger.debug(printer)
                                        if job_in_printers.get(printer, 0) == 0 and not last_used_printer == printer:
                                            logger.debug(f'Using {printer}')
                                            print_file(printer, print_program, config.print_command, join(config.source_path, file))
                                            last_used_printer = printer
                                            logger.info(f'File {file} sent to printer {printer}')
                                        if not job_in_printers.get(printer, 0) == 0 and job_in_printers.get(printer, 0) == last_job_in_printers.get(printer, 0):
                                            logger.debug('Reset last print value')
                                            last_used_printer = ''
                                file_handler.file_move_copy(config.source_path, config.destin_path, file, False)
                            except Exception as error:
                                logger.warning(f'Print fail due {error}')
                                fail_list.append(file)
                            sleep(config.print_interval)
                            last_job_in_printers = job_in_printers
                    logger.info('Waiting...')
                    for _ in range(config.wait_time):
                        if event.is_set():
                            logger.info('Terminanting Print Manager')
                            return                    
                        sleep(1)
                except Exception as error:
                    logger.warning(error)
            else:
                logger.info('Out of set print time')
                for _ in range(config.wait_time):
                    if event.is_set():
                        logger.info('Terminanting Print Manager')
                        return                    
                    sleep(1)                  


def print_manager(database: Database, event: Event, start_delay: int=3) -> None:
    '''
    Start main function to manage files to printers
    '''
    logger.info('Print Manager')

    if event.is_set():
        return
    try:
        config = database.config.get('config')
    except Exception as error:
        logger.critical(f'Could not load config file due {error}')
        event.set()
        return
    
    if start_delay:
        logger.info(f'Initialization delay: {start_delay} seconds...')
        for _ in range(config.start_delay):
            if event.is_set():
                return
            sleep(1)
    print_manager_main(event, config)

