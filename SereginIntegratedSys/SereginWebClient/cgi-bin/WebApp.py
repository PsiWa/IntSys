import time
import message as msg


class WebApp:
    def __init__(self):
        self.ActiveUsers = dict()
        self.username = ""

    def RefreshUsers(self, str):
        self.ActiveUsers.clear()
        buf = str.split(' ')
        for number in range(0, len(buf) - 1, 2):
            self.ActiveUsers[int(buf[number])] = buf[number + 1]


def ProcessMessagesWeb(web):
    while True:
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
        print(msg.Message.ClientID)