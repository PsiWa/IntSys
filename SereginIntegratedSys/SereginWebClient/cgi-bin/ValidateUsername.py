import cgi

#currentdir = os.path.dirname(os.path.realpath(__file__))
#parentdir = os.path.dirname(currentdir)
#sys.path.append(parentdir)
import message as msg
import Chat

q = cgi.FieldStorage()
m = msg.Message.SendMessage(msg.MR_BROKER, msg.MT_INIT, q.getvalue("username"))
print("Content-type: text/html; charset=utf-8\n\n")
if m.Header.hactioncode == msg.MT_DECLINE:
    print("Content-type: text/html; charset=utf-8\n\n")
    print('<h2>Invalid username</h2>')
    with open('./index.html') as f:
        print(f.read())
    exit()
else:
    print(f'<h2>Hello {q.getvalue("username")}!</h2>')
    Chat.main()
    exit()