from os import path
from tkinter import *
from tkinter import messagebox
import os
import json
import time
import math
import sys
start = time.time()
count = 0
time1 = 0
root = Tk()
root['bg']= '#f7f8e7'
root.title('Lab2.py')   
root.wm_attributes('-alpha', 0.7)
root.geometry('600x450')
root.resizable(width = False, height = False)



def check_name(name):
    check_space = 0
    for i in range(len(name)):
        if name[i] == ' ':
            check_space += 1
        if not name[i].isalpha() and name[i] != ' ':
            print("Неверно введено имя, оно должно содержать только буквы")
            return False
    if check_space == 2:
        return True
    else:
        print("Неверно введено имя, оно должно содержать ровно три слова")
        return False

def add_name():
    new_name = get_name.get()
    if not check_name(new_name):
        return False
    else:
        file_path = path.expanduser('~') + '/TIMP/lab2_D1/.namefile/names.json'
        with open(file_path, 'r',encoding='utf-8') as file:
            a = json.load(file)
        if new_name in a['names']:
            messagebox.showerror(title='Ошибка', message='Такое ФИО уже есть в списке')
        else:
            a['names'].append(new_name)
            messagebox.showinfo(title='Информация', message='ФИО успешно добавлено')
            with open(file_path, 'w') as file:
                json.dump(a, file, ensure_ascii=False)


def show_name():
    file_path = path.expanduser('~') + '/TIMP/lab2_D1/.namefile/names.json'
    if path.exists(file_path):
        with open(file_path, 'r') as file:
            try:
                a = json.load(file)
                if 'names' in a and len(a['names']) > 0:
                    for elem in a['names']:
                        print(elem)
                else:
                    print('Список имен пуст')
            except json.JSONDecodeError as e:
                print(f'Ошибка при чтении JSON: {e}')
    else:
        print('Файл не существует или путь некорректен')


def exit():
    if (count > 0 and (time.time() - start) < time1):
        messagebox.showinfo(title='Информация', message=f'Количество запусков осталось: {count}')
        messagebox.showinfo(title='Информация', message=f'Времени пробного периодо программы осталось: {math.ceil(time1 + start - time.time())}')
        with open(path.expanduser('~') + '/.setups1/.files1', 'w') as fil:
            fil.seek(0)
            fil.writelines([str(count), "\n", str(math.ceil(time1 + start - time.time()))])
        sys.exit()
    elif (time.time() - start > time1):
        messagebox.showerror(title='Ошибка', message='Лицензия закончилась(По времени). Купите полную версию программы или удалить её. Чтобы пользоваться прогрммой дальше')
        with open(path.expanduser('~') + '/.setups1/.files1', 'w') as fil:
            fil.seek(0)
            fil.writelines([str(count), "\n", str(math.ceil(time1 + start - time.time()))])
        sys.exit()
    elif (count <= 0):
        messagebox.showerror(title='Ошибка', message='Лицензия закончилась(Количество запусков). Купите полную версию программы или удалить её. Чтобы пользоваться прогрммой дальше')
        with open(path.expanduser('~') + '/.setups1/.files1', 'w') as fil:
            fil.seek(0)
            fil.writelines([str(count), "\n", str(math.ceil(time1 + start - time.time()))])
        sys.exit()
def main():
    global count, time1
    with open(path.expanduser('~') + '/.setups1/.files1', 'r') as fil:
        count, time1 = fil.readlines()
        count = int(count)
        time1 = int(math.ceil(float(time1)))
        count -= 1
        if count <= 0:
            window = Tk()
            window.withdraw()# Спрятать окно
            messagebox.showerror(title='Ошибка', message='Лицензия закончилась(Количество запусков). Купите полную версию программы или удалить её. Чтобы пользоваться прогрммой дальше')
            sys.exit()
        if time.time() - start > time1:
            window1 = Tk()
            window1.withdraw()# Спрятать окно
            messagebox.showerror(title='Ошибка', message='Лицензия закончилась(По времени). Купите полную версию программы или удалить её. Чтобы пользоваться прогрммой дальше')
            sys.exit()
        root.mainloop()
        
      
label_1 = Label(root, text='Основное меню использоваения приложения',
                bg = '#E6E6FA', fg = 'black', font=('Arial', 15, 'bold'),
                width=50, height=4)
label_1.pack()

btn1 = Button (root, text='Добавить новое имя', 
                command=add_name, height= 1
                , width=20)
btn1.place(x=24, y=110)

btn2 = Button (root, text='Показать имеющиеся имена',
                command=show_name, height=1, width=30)
btn2.place (x=24, y=165)


btn3 = Button(root, text='Выйти из программы',
                command=exit, height=1, width=20)
btn3.place(x=24, y=215)

get_name = Entry(root, width=20)
get_name.place(x= 220, y=110)
custom_font = ("Arial", 15)
get_name.config(font=custom_font)
if __name__ == "__main__":
    main()
