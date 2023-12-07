import tkinter as tk
from tkinter import messagebox

import sql
import main

mysql = sql.Sql()


def dl():
    global T
    s = 'select 用户名,密码 from user;'
    value = mysql.select(s)
    for i in value:
        if text.get() == i[0] and psw.get() == i[1]:
            T = True
            break
        else:
            T = False
    if T:
        boot.destroy()
        boot.quit()
        main.window()
    else:
        messagebox.askokcancel("登陆失败", "账号或密码错误，请重新输入！！")


def clear():
    text.delete(0, 'end')
    psw.delete(0, 'end')


boot = tk.Tk()
boot.title('停车场管理系统用户登录')
boot.geometry('400x300+200+200')

login = tk.Frame(boot)
login.pack()

lblmsg = tk.Label(login, text='用户登录', width=25, height=3, font=('', 12))
lblmsg.grid(row=0, column=0, columnspan=2)
username = tk.Label(login, text='用户名')
username.grid(row=1, column=0)
text = tk.Entry(login, width=20)
text.grid(row=1, column=1)

password = tk.Label(login, text='密码')
password.grid(row=2, column=0)
psw = tk.Entry(login, show='*')
psw.grid(row=2, column=1)


denglu = tk.Button(login, width=10, text='登录', command=dl)
denglu.grid(row=3, column=0)
chongxie = tk.Button(login, width=10, text='重写', command=clear)
chongxie.grid(row=3, column=1)

boot.mainloop()


if __name__ == '__main__':
    dl()
