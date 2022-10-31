import cgi
import threading
import time
import message as msg
from tkinter import messagebox
from tkinter import *
from http.server import HTTPServer, BaseHTTPRequestHandler

class WebApp:
    def __init__(self):
        self.ActiveUsers = dict()
        self.username = ""

    def RefreshUsers(self, str):
        self.ActiveUsers.clear()
        buf = str.split(' ')
        for number in range(0, len(buf) - 1, 2):
            self.ActiveUsers[int(buf[number])] = buf[number + 1]

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
                t = threading.Thread(target=ProcessMessagesApp, args=(self.app,))
                t.start()
                self.usrwnd.grab_release()
                self.usrwnd.destroy()


def ProcessMessagesApp(app):
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

web = WebApp()

def ProcessMessagesWeb(web):
    print('ProcessMessagesWeb started')
    while True:
        print(msg.Message.ClientID)
        m = msg.Message.SendMessage(msg.MR_BROKER, msg.MT_REFRESH, str(len(web.ActiveUsers)))
        if m.Header.hactioncode != msg.MT_DECLINE:
            web.RefreshUsers(str(m.Data))
        m = msg.Message.SendMessage(msg.MR_BROKER, msg.MT_GETDATA)
        if m.Header.hactioncode == msg.MT_DATA:
            print(f"{web.ActiveUsers[m.Header.hfrom]}: {m.Data}")
        elif m.Header.hactioncode == msg.MT_EXIT:
            m = msg.Message.SendMessage(msg.MR_BROKER, msg.MT_EXIT)
        else:
            time.sleep(1)


test = 'aaaa'


class requestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('content-type', 'text/html')
        self.end_headers()
        output = '''<html>
                    <head>
                    <title>TRIS Chat</title>
                    </head>
                    <body>
                    <h3>Enter username</h3>
                    <form method="POST" enctype="multipart/form-data"">
                    <br><input type=text name=username size=50>
                    <input type=submit value="Send">'''
        output+=f'<li>{test}</li>'
        output += '</ul>'
        self.wfile.write(output.encode())

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers['content-type'])
        pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
        content_len = int(self.headers.get('Content-length'))
        pdict['Content-Length'] = content_len
        self.send_response(301)
        self.send_header('content-type', 'text/html')
        self.send_header('Location', '/')
        if ctype == 'multipart/form-data':
            fields = cgi.parse_multipart(self.rfile, pdict)
            m = msg.Message.SendMessage(msg.MR_BROKER, msg.MT_INIT, fields.get("username")[0])
            if m.Header.hactioncode != msg.MT_DECLINE:
                print('success')
            else:
                print('error')
        self.end_headers()


def ProcessServer():
    server_address = ("", 8080)
    print("Web interface started")
    HTTPServer(server_address, requestHandler).serve_forever()




def main():
    '''app = MainWindow();
    app.UsrList.insert(1, 'All users')
    # msg.Message.SendMessage(msg.MR_BROKER, msg.MT_INIT, 'pyuser')
    UsernameWindow(app)
    app.root.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.root.mainloop()'''
    print("Python client has started\n")
    w = threading.Thread(target=ProcessServer)
    w.start()
    t = threading.Thread(target=ProcessMessagesWeb(web))
    t.start()


if __name__ == '__main__':
    main()
