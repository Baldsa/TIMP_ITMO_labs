import pyAesCrypt
import hashlib

import glob
import json
import os, sys

from threading import Thread
import time

global stop
stop = False


def def_up(password): #Поднимаем защиту
    bufferSize = 64 * 1024 # Буффер для пароля
    if 'template.tbl.enc' in os.listdir(): 
        pyAesCrypt.decryptFile('template.tbl.enc', 'template.tbl', password, bufferSize) # Если в прошлый раз файл template.tbl был зашифрован, то нужно его сначала расшифровать.
    
    # Цикл ниже выполняет шифрование файлов в template.tbl test.txt -> test.txt.enc и после чего удаляется файл test.txt
    with open('template.tbl', 'r') as file:
        fi = json.load(file)
    for i in fi['files']:
        for j in glob.glob(i):
            if (j != 'template.tbl'):
                pyAesCrypt.encryptFile(j, j + ".enc", password, bufferSize)
                os.remove(j)

    files = fi['files']
    # Выставляем права на неизменяемость файла, а также запрет на чтение и изменение.
    with open('template.tbl', 'r') as file:
        fi = json.load(file)
    for i in fi['files']:
        for j in glob.glob(i + '.enc'):
            print(j)
            os.chmod(j, 0o000)
            os.system(f"sudo -S chattr +i {j}")
    #Шифруем сам файл template.tbl 
    pyAesCrypt.encryptFile('template.tbl', 'template.tbl.enc', password, bufferSize)
    os.remove('template.tbl')
    os.system(f"sudo -S chattr +i template.tbl.enc")
    return files

def def_down(password):
    bufferSize = 64 * 1024
    os.system(f"sudo -S chattr -i template.tbl.enc")
    
    if 'template.tbl.enc' in os.listdir():
        pyAesCrypt.decryptFile('template.tbl.enc', 'template.tbl', password, bufferSize)
        os.remove('template.tbl.enc')
    #set rights
    with open('template.tbl', 'r') as file:
        fi = json.load(file)
    for i in fi['files']:
        for j in glob.glob(i):
            os.system(f"sudo -S chattr -i {j}")
            os.chmod(j, 0o777)
        for j in glob.glob(i + '.enc'):
            os.system(f"sudo -S chattr -i {j}")
            os.chmod(j, 0o777)
    #decrypt files
    for i in fi['files']:
        for j in glob.glob(i + '.enc'):
            pyAesCrypt.decryptFile(j, '.'.join(j.split('.')[0:-1]), password, bufferSize)
            os.remove(j)

def checker(files):
    global stop
    while True:
        time.sleep(5)
        if stop:
            return 0
        for i in files:
            for j in glob.glob(i):
                if '.enc' not in j:
                    os.remove(j)
            
def set_new_password(password):
    hash_object = hashlib.md5(password.encode())
    with open('template.tbl', 'r') as file:
        old = json.load(file)
    with open('template.tbl', 'w') as file:
        old["password"] = hash_object.hexdigest()
        json.dump(old, file)

flag_path = '/home/balora/moni/flag.txt'
def main():
    global stop
    prev_cmd = 0
    password = '' # pass is 123

    with open((flag_path), 'r') as f:
        flag_start = f.read()
    if not int(flag_start):
        key_str = input('Введите где храниться ваша цифровая подпись ')
        usr_in =  os.environ.get(key_str) 
        pass_in = os.environ.get('kopylov_and_berezina')
        flag_auth = False
        if pass_in == usr_in:
            print('\nЛичность подтверждена\n')
            flag_auth = True
        else:
            print('\nОшибка аутентификации по цифровой подписи\n')
            sys.exit()
    password = input("Enter the password:")
    if ('template.tbl.enc' in os.listdir()):
        try: 
            pyAesCrypt.decryptFile('template.tbl.enc', 'template.tbl', password, 64*1028)
        except:
            print('\nПароль неверен!!!\n')
            sys.exit()
    else:
        with open('template.tbl', 'r') as f:
            fi = json.load(f)
            if hashlib.md5(password.encode()).hexdigest() != fi['password']:
                    print('\nПароль неверен!!!\n')
                    sys.exit()
    while True:
        cmd = int(input("1 -> Включить защиту\n2 -> Отключить защиту\n3 -> Выход\n"))
        if cmd == 1 and prev_cmd != 1:
            files = def_up(password)
            my_thread = Thread(target=checker, args=(files,))
            my_thread.start()
            flag=True
        elif cmd == 2 and prev_cmd != 2:
            print('ok')
            def_down(password)
            stop = True      
            flag=True
        elif cmd == 3:
            stop = True
            sys.exit()
        prev_cmd = cmd
main()
