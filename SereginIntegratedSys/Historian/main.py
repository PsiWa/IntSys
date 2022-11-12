import sqlite3
import os
import message as msg
import socket

def init_database():
    con = sqlite3.connect("Users.db")
    cur = con.cursor()
    cur.execute("CREATE TABLE user(id INTEGER PRIMARY KEY,username VARCHAR UNIQUE NOT NULL, password VARCHAR)")
    res = cur.execute("SELECT name FROM sqlite_master")
    print(f"{res.fetchone()} db was created")
    cur.execute("""
            INSERT INTO user VALUES
                (0,"MR_ALL",""),
                (1,"MR_BROKER",""),
                (2,"MR_HISTORIAN",""),
                (100,"MR_USER","")
                """)
    con.commit()


def main():
    if not os.path.isfile("Users.db"):
        init_database()
    else:
        con = sqlite3.connect("Users.db")
        cur = con.cursor()
        users = dict()
        for row in cur.execute("SELECT id,username FROM user"):
            (id,username) = row
            users[id]=username
        HOST = 'localhost'
        PORT = 12345
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            m = msg.Message(msg.MR_BROKER, msg.MT_INIT)
            m.Send(s)
            m.Receive(s)
            print("connected to broker")
            #t = threading.Thread(target=WriteHistory(), args=(s,))
            #t.start()
            while True:
                m.Receive(s)
                if m.Header.hactioncode == msg.MT_INIT:
                    id = 0
                    buf = m.Data.split(' ')
                    res = cur.execute(f"""SELECT id,password FROM user WHERE username = '{buf[0]}'""")
                    try:
                        (id,password)  = res.fetchone()
                    except TypeError:
                        id = 0
                    if id ==0 :
                        cur.execute("""INSERT INTO user (username,password) VALUES (?,?)""", (buf[0],buf[1]))
                        con.commit()
                        res = cur.execute(f"""SELECT id,password FROM user WHERE username = '{buf[0]}'""")
                        try:
                            (id, password) = res.fetchone()
                            m = msg.Message(msg.MR_BROKER, msg.MT_CONFIRM, str(id) + " " + buf[0])
                            m.Send(s)
                            users[id]=buf[0]
                        except TypeError:
                            m = msg.Message(msg.MR_BROKER, msg.MT_DECLINE)
                            m.Send(s)
                    else:
                        if str(buf[1]) == str(password):
                            m = msg.Message(msg.MR_BROKER, msg.MT_CONFIRM, str(id) + " "+buf[0])
                            m.Send(s)
                        else:
                            m = msg.Message(msg.MR_BROKER, msg.MT_DECLINE)
                            m.Send(s)
                elif m.Header.hactioncode == msg.MT_REFRESH:
                    read_data = "Message history:\n"
                    with open('History/0.dat', encoding="utf-8") as f:
                        read_data += f.read()
                    f.close()
                    read_data+="Private messages:\n"
                    try:
                        with open(f'History/{m.Header.hfrom}.dat', encoding="utf-8") as f:
                            read_data += f.read()
                        f.close()
                    except FileNotFoundError:
                        read_data += "There are no private messages for you\n"
                    m = msg.Message(msg.MR_BROKER, msg.MT_CONFIRM, read_data)
                    m.Send(s)
                elif m.Header.hactioncode == msg.MT_DATA:
                    if m.Header.haddr == msg.MR_ALL:
                        with open('History/0.dat','a', encoding="utf-8") as f:
                            f.write(f"{users[m.Header.hfrom]}:{m.Data}\n")
                        f.close()
                    else:
                        with open(f'History/{m.Header.haddr}.dat','a', encoding="utf-8") as f:
                            f.write(f"{users[m.Header.hfrom]}:{m.Data}\n")
                        f.close()


if __name__ == '__main__':
    main()