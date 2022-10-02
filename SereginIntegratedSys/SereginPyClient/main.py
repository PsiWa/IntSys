import sys
import threading
from dataclasses import dataclass
import socket, struct, time
from tkinter import messagebox
import message as msg
from tkinter import *


class MainWindow:
    def __init__(self):
        self.username = ""
        self.ActiveUsers = dict()
        self.root = Tk()
        self.frame1 = Frame(self.root)
        self.frame2 = Frame(self.root)
        self.MsgList = Listbox(self.frame1, width=100, height=100)
        self.UsrList = Listbox(self.frame1, width=50, height=100)
        self.SendBtn = Button(self.frame2, text='Send', command=self.btn_click, width=20, height=1)
        self.MsgInput = Entry(self.frame2, width=70)
        self.InitUI();

    def InitUI(self):
        self.root['bg'] = '#FFFAFA'
        self.root.title('PyClient')
        self.root.geometry('820x430')
        self.root.resizable(width=False, height=False)

        self.frame1.place(relwidth=1, relheight=0.8)
        self.frame2.place(relwidth=1, relheight=0.2, y=round(430 * 0.8))

        self.MsgList.pack(side=RIGHT)
        self.UsrList.pack(side=RIGHT)
        self.SendBtn.pack(side=RIGHT)
        self.MsgInput.pack(side=RIGHT)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            m = msg.Message.SendMessage(msg.MR_BROKER, msg.MT_EXIT)
            self.root.destroy()

    def btn_click(self):
        recipient = msg.MR_ALL
        message = self.MsgInput.get()
        isPrivate = False
        for key,value in self.ActiveUsers.items():
            if str(self.UsrList.get(ANCHOR)).find(value)!=-1:
                recipient = key
                self.MsgList.insert('end',f"You whispered to {value}: {message}")
                isPrivate = True
                break
        if not isPrivate:
            self.MsgList.insert('end',f"You: {message}")
        m = msg.Message.SendMessage(recipient, msg.MT_DATA, message)
        self.MsgInput.delete(0,'end')

    def RefreshUsers(self, str):
        self.ActiveUsers.clear()
        buf = str.split(' ')
        for number in range(0, len(buf) - 1, 2):
            self.ActiveUsers[int(buf[number])] = buf[number + 1]
        self.UsrList.delete(0,'end')
        self.UsrList.insert(0, 'All Users')
        for key, value in self.ActiveUsers.items():
            if self.username!=value:
                self.UsrList.insert(1, value)


class UsernameWindow:
    def __init__(self, app):
        self.app = app
        self.usrwnd = Toplevel(app.root)
        self.frame = Frame(self.usrwnd)
        self.lbl = Label(self.usrwnd, text='Enter Username')
        self.usrname = Entry(self.usrwnd)
        self.ackbtn = Button(self.usrwnd, command=self.AckUsername, text='Send')
        self.InitUI()

    def InitUI(self):
        self.usrwnd.grab_set()
        self.usrwnd['bg'] = '#FFFAFA'
        self.usrwnd.title('PyClient')
        self.usrwnd.geometry('200x200')
        self.usrwnd.resizable(width=False, height=False)
        self.frame.place(relwidth=1, relheight=1)

        self.lbl.pack()
        self.usrname.pack()
        self.ackbtn.pack()

    def AckUsername(self):
        if (self.usrname.get() != ''):
            m = msg.Message.SendMessage(msg.MR_BROKER, msg.MT_INIT, self.usrname.get())
            if (m.Header.hactioncode == msg.MT_DECLINE):
                messagebox.showerror('Wrong username')
                self.usrname.delete(0, 'end')
            else:
                self.app.username = self.usrname.get()
                self.app.MsgList.insert(1, f"Server: Hello {self.app.username}!")
                t = threading.Thread(target=ProcessMessages, args=(self.app,))
                t.start()
                self.usrwnd.grab_release()
                self.usrwnd.destroy()


def ProcessMessages(app):
    while True:
        m = msg.Message.SendMessage(msg.MR_BROKER, msg.MT_REFRESH, str(len(app.ActiveUsers)))
        if m.Header.hactioncode != msg.MT_DECLINE:
            app.RefreshUsers(str(m.Data))
        m = msg.Message.SendMessage(msg.MR_BROKER, msg.MT_GETDATA)
        if m.Header.hactioncode == msg.MT_DATA:
            app.MsgList.insert('end', f"{app.ActiveUsers[m.Header.hfrom]}: {m.Data}")
        elif m.Header.hactioncode == msg.MT_EXIT:
            m = msg.Message.SendMessage(msg.MR_BROKER, msg.MT_EXIT)
            app.root.destroy()
        else:
            time.sleep(1)


def main():
    app = MainWindow();
    app.UsrList.insert(1, 'All users')
    # msg.Message.SendMessage(msg.MR_BROKER, msg.MT_INIT, 'pyuser')
    UsernameWindow(app)
    app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.root.mainloop()


if __name__ == '__main__':
    main()
