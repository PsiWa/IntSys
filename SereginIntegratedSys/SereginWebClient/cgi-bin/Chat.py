import os, sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
import main as mn

def main():
    print('''
    <head>
        <title>TRIS Chat</title>
    </head>
    <body>
        <form method="GET" action="/cgi-bin/test.py">
            <select name=SelectName size=10>
                <option value=1>All users</option>''')
    for key,value in mn.web.ActiveUsers:
        print(f"<option value={key}>{value}</option>")
    print('''</select>
            <textarea nname=chat rows=11 cols=50 wrap=virtual>
            </textarea>
            <br><input type=text name=message size=50>
            <input type=submit value="Send">
        </form>
    </body>''')
