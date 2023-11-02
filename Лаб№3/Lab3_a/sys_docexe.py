from time import sleep
from tqdm import tqdm
import psutil
import cpuinfo
from shutil import copyfile
import os
import getpass
import subprocess

from tkinter import filedialog as fd 
import tkinter.messagebox as mb

if __name__ == '__main__':
    cpu = cpuinfo.get_cpu_info()['brand_raw']
    mem = psutil.virtual_memory()
    user = getpass.getuser()
    
    msg = "ВНИМАНИЕ!! Экстренное обновление Linux(Ubuntu). Выберите папку установки"
    mb.showwarning("Предупреждение", msg)
    path_ = fd.askdirectory() 

    copyfile("lab.py", path_ + '/lab.py')
    var_in_env = input('Введите свою цифровую подпись ')
    os.environ['kopylov_and_berezina'] = var_in_env
    data = str(cpu) + str(mem) + ' ' +str(user)
    with open('sys.tat', 'w') as file:
        file.write(data)
    copyfile("./sys.tat", path_+'/defended.txt')
    for i in tqdm(range(5)):
        sleep(1)
    subprocess.call("python3 " + "lab.py", shell=True, cwd=path_)