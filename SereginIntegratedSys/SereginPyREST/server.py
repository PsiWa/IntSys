import time
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import json
import message as msg


ActiveUsers = dict()
ActiveUsersString = ""


def RefreshUsers(str):
    global ActiveUsers
    ActiveUsers.clear()
    buf = str.split(' ')
    for number in range(0, len(buf) - 1, 2):
        ActiveUsers[int(buf[number])] = buf[number + 1]

class requestHandler(BaseHTTPRequestHandler):

    def MakeResponse(self, to, From, type, data):
        return '{"to":"' + str(to) + '","type":"' + str(type) + '","data":"' + str(data) + '","from":"' + str(From) + '"}'

    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        content_length = int(self.headers['Content-Length'])  # <--- Gets the size of data
        post_data = self.rfile.read(content_length)
        data = post_data.decode('utf-8')
        data = json.loads(data)
        if int(data['type']) == msg.MT_INIT:
            m = msg.Message.SendMessage(int(data['to']), int(data['type']), data['data'])
            Data=""
            for p in m.Data.split('\n'):
                Data = Data + p + "$&"
            print(Data)
            self.wfile.write(self.MakeResponse(m.Header.haddr, m.Header.hfrom, m.Header.hactioncode, Data).encode())
            print("Rest client " + str(m.Header.haddr) + " entered")
        elif int(data['type']) == msg.MT_REFRESH:
            if int(data['data']) != len(ActiveUsers):
                self.wfile.write(self.MakeResponse(int(data['from']), msg.MR_BROKER, msg.MT_REFRESH, str(ActiveUsersString)).encode())
            else:
                self.wfile.write(self.MakeResponse(int(data['from']), msg.MR_BROKER, msg.MT_DECLINE,"").encode())
        else:
            m = msg.Message.SendAsClient(int(data['to']), int(data['from']), int(data['type']), data['data'])
            self.wfile.write(self.MakeResponse(m.Header.haddr, m.Header.hfrom, m.Header.hactioncode, m.Data).encode())


def ProcessServer():
    server_address = ("", 8000)
    print("Rest support server has started")
    HTTPServer(server_address, requestHandler).serve_forever()

def ProcessMessages():
    global ActiveUsers
    global ActiveUsersString
    print('ProcessMessages started')
    while True:
        m = msg.Message.SendAsClient(msg.MR_BROKER, msg.MR_REST, msg.MT_REFRESH, str(len(ActiveUsers)))
        if m.Header.hactioncode != msg.MT_DECLINE:
            ActiveUsersString = str(m.Data)
            RefreshUsers(str(m.Data))
        else:
            time.sleep(1)
        #m = msg.Message.SendMessage(msg.MR_BROKER, msg.MT_GETDATA)
        #if m.Header.hactioncode == msg.MT_DATA:
        #    print(f"{ActiveUsers[m.Header.hfrom]}: {m.Data}")
        #elif m.Header.hactioncode == msg.MT_EXIT:
        #    m = msg.Message.SendMessage(msg.MR_BROKER, msg.MT_EXIT)


def RestServer():
    w = threading.Thread(target=ProcessServer)
    w.start()
    t = threading.Thread(target=ProcessMessages)
    t.start()

if __name__ == '__main__':
    RestServer()