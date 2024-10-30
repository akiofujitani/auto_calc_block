r"""
pyinstaller --noconfirm --onefile --windowed --icon "C:\Users\faust\OneDrive\Documentos\Development\auto_calc_block\Img\black-cat.png" --name "Automatic Calculation Blocker" --add-data "C:\Users\faust\OneDrive\Documentos\Development\auto_calc_block\Img;Img/"  "C:\Users\faust\OneDrive\Documentos\Development\auto_calc_block\root\main.py"

"""

# from datetime import time

# time_value = time(18, 00)

# time_str_test = '15:00'
# time_test = time.strftime(time_value, '%H:%m')
# print(time_test)
# str_time = f'{time_value.hour:02d}:{time_value.minute:02d}' 
# print(str_time)

# new_time = time(*[int(value) for value in str_time.split(':')])

# if isinstance(new_time, time):
#     print('Type time')


str_test = 'test\nline 2\n'

remove_break = str_test.rstrip()

print(str_test)
print(remove_break)