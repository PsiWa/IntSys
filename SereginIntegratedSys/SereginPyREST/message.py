import threading
from dataclasses import dataclass
import socket, struct, time

MT_INIT = 0
MT_EXIT = 1
MT_GETDATA = 2
MT_DATA = 3
MT_NODATA = 4
MT_CONFIRM = 5
MT_DECLINE = 6
MT_REFRESH = 7

MR_BROKER = 1
MR_ALL = 0
MR_USER = 100
MR_REST = 3


@dataclass
class MessageHeader:
    haddr: int = 0
    hfrom: int = 0
    hactioncode: int = 0
    hsize: int = 0

    def Send(self, s):
        s.send(struct.pack(f'iiii', self.haddr, self.hfrom, self.hactioncode, self.hsize))

    def Receive(self, s):
        try:
            (self.haddr, self.hfrom, self.hactioncode, self.hsize) = struct.unpack('iiii', s.recv(16))
        except:
            self.hsize = 0
            self.hactioncode = MT_NODATA


class Message:
    ClientID = 0

    def __init__(self, To=0, From=0, Action=MT_DATA, Data=""):
        self.Header = MessageHeader(To, From, Action, len(Data))
        self.Data = Data

    def Send(self, s):
        self.Header.Send(s)
        if self.Header.hsize > 0:
            s.send(struct.pack(f'{self.Header.hsize}s', self.Data.encode('cp866')))

    def Receive(self, s):
        self.Header.Receive(s)
        if self.Header.hsize > 0:
            self.Data = struct.unpack(f'{self.Header.hsize}s', s.recv(self.Header.hsize))[0].decode('cp866')

    def SendMessage(To, Action=MT_DATA, Data=""):
        HOST = 'localhost'
        PORT = 12345
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            m = Message(To, Message.ClientID, Action, Data)
            m.Send(s)
            m.Receive(s)
            if m.Header.hactioncode == MT_INIT:
                Message.ClientID = m.Header.haddr
            return m

    def SendAsClient(To, From, Type=MT_DATA, Data=""):
        HOST = 'localhost'
        PORT = 12345
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            m = Message(To, From, Type, Data)
            if m.Header.hfrom == m.Header.haddr:
                print("You can't send message to yoursef")
            else:
                m.Send(s)
                m.Receive(s)
                return m
