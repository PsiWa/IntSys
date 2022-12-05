import threading
import socket, struct, time
from tkinter import messagebox
import requests
import message as msg
from tkinter import *


def SendRequest(params):
    URL = "http://localhost:8000"
    r = requests.get(url=URL, json=params)
    return r.json()


class MainWindow:
    def __init__(self):
        self.username = ""
        self.id = 0;
        self.ActiveUsers = dict()
        self.root = Tk()
        self.frame1 = Frame(self.root)
        self.frame2 = Frame(self.root)
        self.MsgList = Listbox(self.frame1, width=100, height=100)
        self.UsrList = Listbox(self.frame1, width=50, height=100)
        self.SendBtn = Button(self.frame2, text='Send', command=self.btn_click, width=20, height=1)
        self.MsgInput = Entry(self.frame2, width=70)
        self.InitUI();

    def SendInit(self,username,password):
        resp = SendRequest({'to': msg.MR_BROKER, 'from': '', 'type': msg.MT_INIT, 'data': username + " "+password})
        return resp

    def Send(self, id, message):
        a = SendRequest({'to': id, 'from': self.id, 'type': msg.MT_DATA, 'data': message})

    def SendAll(self, message):
        a = SendRequest({'to': msg.MR_ALL, 'from': self.id, 'type': msg.MT_DATA, 'data': message})

    def SendExit(self):
        a = SendRequest({'to': msg.MR_BROKER, 'from': self.id, 'type': msg.MT_EXIT, 'data': ''})

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
            self.SendExit()
            self.root.destroy()

    def btn_click(self):
        recipient = msg.MR_ALL
        message = self.MsgInput.get()
        isPrivate = False
        for key,value in self.ActiveUsers.items():
            if str(self.UsrList.get(ANCHOR)).find(value)!=-1:
                recipient = key
                self.MsgList.insert('end',f"You whispered to {value}: {message}")
                message = "(private) "+message
                isPrivate = True
                break
        if not isPrivate:
            self.MsgList.insert('end',f"You: {message}")
        self.Send(recipient,message)
        #m = msg.Message.SendMessage(recipient, msg.MT_DATA, message)
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
        self.lbl1 = Label(self.usrwnd, text='Enter Username')
        self.usrname = Entry(self.usrwnd)
        self.lbl2 = Label(self.usrwnd, text='Enter Password')
        self.password = Entry(self.usrwnd,show="*")
        self.ackbtn = Button(self.usrwnd, command=self.AckUsername, text='Send')
        self.InitUI()

    def InitUI(self):
        self.usrwnd.grab_set()
        self.usrwnd['bg'] = '#FFFAFA'
        self.usrwnd.title('PyClient')
        self.usrwnd.geometry('200x200')
        self.usrwnd.resizable(width=False, height=False)
        self.frame.place(relwidth=1, relheight=1)

        self.lbl1.pack()
        self.usrname.pack()
        self.lbl2.pack()
        self.password.pack()
        self.ackbtn.pack()

    def AckUsername(self):
        if (self.usrname.get() != ''):
            a = self.app.SendInit(self.usrname.get(),self.password.get())
            if int(a['type'])==msg.MT_DECLINE:
                messagebox.showerror('Error','Wrong username or password')
                self.usrname.delete(0, 'end')
                self.password.delete(0, 'end')
            else:
                self.app.username = self.usrname.get()
                for p in a['data'].split('$&'):
                    self.app.MsgList.insert('end', p)
                self.app.MsgList.insert('end', f"Server: Hello {self.app.username}!")
                self.app.id = int(a['to'])
                t = threading.Thread(target=ProcessMessagesREST, args=(self.app,))
                t.start()
                self.usrwnd.grab_release()
                self.usrwnd.destroy()


def ProcessMessagesREST(app):
    while True:
        a = SendRequest({'to': msg.MR_BROKER, 'from': app.id, 'type': msg.MT_REFRESH, 'data': str(len(app.ActiveUsers))})
        if int(a['type']) != msg.MT_DECLINE:
            app.RefreshUsers(a['data'])
            print('Refreshed '+a['data'])
            print(len(app.ActiveUsers))
        a = SendRequest({'to': msg.MR_BROKER, 'from': app.id, 'type': msg.MT_GETDATA, 'data': ''})
        if int(a['type']) == msg.MT_DATA:
            print("New message: " + a['data'] + "\nFrom: " + a['from'])
            app.MsgList.insert('end', f"{app.ActiveUsers[int(a['from'])]}: {a['data']}")
        elif int(a['type']) == msg.MT_EXIT:
            app.SendExit()
            app.root.destroy()
        else:
            time.sleep(1)


def main():
    app = MainWindow()
    app.UsrList.insert(1, 'All users')
    UsernameWindow(app)
    app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.root.mainloop()

if __name__ == '__main__':
    main()
