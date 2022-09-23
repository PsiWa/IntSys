// SereginCLIClient.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include "pch.h"
#include "framework.h"
#include "SereginCLIClient.h"
#include "../SereginIntegratedSys/Message.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif
#include <atlcom.h>

map<int, string> ActiveUsers;
CCriticalSection cs;
string username = "";

void HistoryWrite(string str,string& uname)
{
    cs.Lock();
    ofstream hist("history"+uname+".dat", ios::app);
    if (hist.is_open())
    {
        hist << str << endl;;
        hist.close();
    }
    cs.Unlock();
}

void HistoryRead(string& uname)
{
    string line;
    cs.Lock();
    ifstream hist("history"+uname+".dat", ios::out);
    if (hist.is_open())
    {
        while (getline(hist,line))
        {
            cout << line << endl;
        }
        hist.close();
    }
    cs.Unlock();
}

void PrintActiveUsers()
{
    cout << "__________________________________________\nActive Users :" << endl;
    for (auto& user : ActiveUsers)
    {
        cout << user.second << "(" << user.first << "); ";
    }
    cout << endl;
}

void RefreshActiveUsers(string str)
{
    ActiveUsers.clear();
    stringstream NamesAndIds(str);
    while (true)
    {
        int uid;
        string uname;
        NamesAndIds >> uid;
        if (int(uid) == -1)
            break;
        NamesAndIds >> uname;
        ActiveUsers[int(uid)] = uname;
    }
}

int CheckCommands(string& str)
{
    if (str == "/help")
        return 3;
    if (str == "/exit")
        return 1;
    auto pos = str.find("/whisper");
    if (pos != str.npos)
    {
        str = str.erase(pos, size("/whisper"));
        for (auto user : ActiveUsers)
        {
            pos = str.find(user.second);
            if (pos != str.npos)
            {
                str = str.erase(pos, user.second.length()+1);
                return user.first;
            }
        }
        return 2;
    } 
    if (str == "/reconect")
        return 4;
    return 0;
}

void ProcessMessages()
{
    bool ExitFlag = true;
    while (ExitFlag)
    {
        Message m = Message::Send(MR_BROKER, MT_REFRESH,to_string(ActiveUsers.size()));
        if (m.GetAction() != MT_DECLINE)
        {
            RefreshActiveUsers(m.GetData());
            cout << string(100, '\n') << endl;
            HistoryRead(username);
            PrintActiveUsers();
        }
        m = Message::Send(MR_BROKER, MT_GETDATA);
        switch (m.GetAction())
        {
        case MT_DATA:
        {
            HistoryWrite((ActiveUsers[m.GetFrom()] + ": " + m.GetData()),username);
            cout << string(100, '\n') << endl;
            HistoryRead(username);
            PrintActiveUsers();
            break;
        }
        case MT_EXIT:
            cout << "You've been disconected from the server" << endl;
            m = Message::Send(MR_BROKER, MT_EXIT);
            ExitFlag = false;
        default:
            Sleep(1000);
            break;
        }
    }
    cout << "Please reconect" << endl;
}

int Client()
{
    AfxSocketInit();
    
    while (true)
    {
        cout << "Enter User Name" << endl;
        cin >> username;
        Message m = Message::Send(MR_BROKER, MT_INIT, username);
        if (m.GetAction() == MT_DECLINE)
        {
            cout << "Invalid User Name" << endl;
        }
        else
        {
            HistoryWrite("server: Hello "+username, username);
            cout << string(100, '\n') << endl;
            RefreshActiveUsers(m.GetData());
            HistoryRead(username);
            PrintActiveUsers();
            break;
        }
    }
    cin.ignore();
    thread t(ProcessMessages);
    t.detach();

    while (true)
    {
        string str;
        cin.clear();
        getline(cin,str);
        cout << str << "-1" << endl;
        int com = CheckCommands(str);
        switch(com)
        {
        case 0:
        {
            HistoryWrite("You: " + str, username);
            Message::Send(MR_ALL, MT_DATA, str);
            cout << string(100, '\n') << endl;
            HistoryRead(username);
            PrintActiveUsers();
            break;
        }
        case 1:
        {
            Message::Send(MR_BROKER, MT_EXIT);
            return 0;
            break;
        }
        case 2:
        {
            cout << "Error" << endl;;
            break;
        }
        case 3:
        {
            cout << "Type:\n/exit to exit;\n/reconect to reconect to the server;\n/whisper [UserName] [Message] to send private message" << endl;
            break;
        }
        case 4:
        {
            Message::Send(MR_BROKER, MT_EXIT);
            return 1;
            break;
        }
        default:
        {
            HistoryWrite("You whisperd to " + to_string(com) + ": " + str, username);
            Message::Send(com, MT_DATA, str);
            cout << string(100, '\n') << endl;
            HistoryRead(username);
            PrintActiveUsers();
            break;
        }
        }
    }

}
// Единственный объект приложения

CWinApp theApp;

using namespace std;

int main()
{
    int nRetCode = 0;

    HMODULE hModule = ::GetModuleHandle(nullptr);

    if (hModule != nullptr)
    {
        // инициализировать MFC, а также печать и сообщения об ошибках про сбое
        if (!AfxWinInit(hModule, nullptr, ::GetCommandLine(), 0))
        {
            // TODO: вставьте сюда код для приложения.
            wprintf(L"Критическая ошибка: сбой при инициализации MFC\n");
            nRetCode = 1;
        }
        else
        {
            int ExitCode = 1;
            while (ExitCode != 0)
                ExitCode = Client();
            if (remove(("history"+username+".dat").c_str()) != 0)
                perror("Error deleting file");
            else
                puts("File successfully deleted");
            // TODO: вставьте сюда код для приложения.
        }
    }
    else
    {
        // TODO: измените код ошибки в соответствии с потребностями
        wprintf(L"Критическая ошибка: сбой GetModuleHandle\n");
        nRetCode = 1;
    }

    return nRetCode;
}
