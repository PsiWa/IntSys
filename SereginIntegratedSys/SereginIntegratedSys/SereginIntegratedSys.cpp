// SereginIntegratedSys.cpp : Этот файл содержит функцию "main". Здесь начинается и заканчивается выполнение программы.
//

#include "pch.h"
#include "framework.h"
#include "SereginIntegratedSys.h"
#include "Message.h"
#include "Session.h"

#ifdef _DEBUG
#define new DEBUG_NEW
#endif


//extern "C"
//{
//    class AFX_EXT_CLASS Message;
//
//    __declspec(dllimport) void _stdcall StartServer();
//
//    __declspec(dllimport) void _stdcall StopServer();
//
//    __declspec(dllimport) bool _stdcall ServerListen(CSocket* s);
//}
// Единственный объект приложения

CWinApp theApp;
using namespace std;

void LaunchClient()
{
    STARTUPINFO si = { sizeof(si) };
    PROCESS_INFORMATION pi;
    CreateProcess(NULL, (LPSTR)"SereginCLIClient.exe", NULL, NULL, TRUE, CREATE_NEW_CONSOLE, NULL, NULL, &si, &pi);
    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
}

int maxID = MR_USER;
map<int, shared_ptr<Session>> sessions;
CCriticalSection cs;

string GetActiveUsers()
{
    string NamesAndIds = "";
    for (auto& session : sessions)
    {
        NamesAndIds = NamesAndIds +to_string(session.second->id) + " " + session.second->GetName() + " ";
    }
    return NamesAndIds;
}

void CheckIfUserIsInactive()
{
    int timespan = 30000;
    while (true)
    {
        if (sessions.size() > 0)
        {
            for (auto& session: sessions)
            {
                if (chrono::duration_cast<chrono::milliseconds>(chrono::steady_clock::now()
                    - session.second->GetLastSeen()).count() > timespan)
                {
                    Message m(session.second->id, MR_BROKER, MT_EXIT);
                    session.second->MessageAdd(m);
                    cout << session.second->id << " AFK" << endl;
                }
                if (chrono::duration_cast<chrono::milliseconds>(chrono::steady_clock::now()
                    - session.second->GetLastSeen()).count() > timespan * 2)
                {
                    cout << "Session " + to_string(session.first) + "deleted" << endl;
                    sessions.erase(session.first);
                    break;
                }
            }
        }
        cout << "CheckIfUserIsInactive() sleeping" << endl;
        Sleep(timespan);
    }
}

void ClientProcessing(SOCKET hSock)
{
    CSocket s;
    s.Attach(hSock);
    Message m;
    int code = m.Receive(s);
    switch (code)
    {
    case MT_INIT:
    {
        bool isDeclined = false;
        for (auto& [id, iSession] : sessions)
        {
            if (iSession->GetName() == m.GetData())
            {
                Message::Send(s, 0, MR_BROKER, MT_DECLINE);
                isDeclined = true;
                cout << "error" << endl;
            }
        }
        if (!isDeclined)
        {
            auto session = make_shared<Session>(++maxID, m.GetData());
            sessions[session->id] = session;
            Message::Send(s, session->id, MR_BROKER, MT_INIT, (GetActiveUsers() + "-1"));
            cout << session->id << " (" << session->GetName() << ") connected" << endl;
            session->SetLastSeen();
        }
        break;
    }
    case MT_EXIT:
    {
        sessions.erase(m.GetFrom());
        Message::Send(s, m.GetFrom(), MR_BROKER, MT_CONFIRM);
        cout << m.GetFrom() << " exited" << endl;
        break;
    }
    case MT_GETDATA:
    {
        auto iSession = sessions.find(m.GetFrom());
        if (iSession != sessions.end())
        {
            iSession->second->MessageSend(s);
        }
        break;
    }
    case MT_REFRESH:
    {
        if (stoi(m.GetData()) != int(sessions.size()))
        {
            auto iSession = sessions.find(m.GetFrom());
            if (iSession != sessions.end())
            {
                Message::Send(s, iSession->second->id, MR_BROKER, MT_REFRESH, (GetActiveUsers() + "-1"));
                cout << iSession->second->id << " refreshed" << endl;
            }
        }
        else
            Message::Send(s, m.GetFrom(), MR_BROKER, MT_DECLINE);
        break;
    }
    default:
    {
        auto iSessionFrom = sessions.find(m.GetFrom());
        if (iSessionFrom != sessions.end())
        {
            iSessionFrom->second->SetLastSeen();
            auto iSessionTo = sessions.find(m.GetAddr());
            if (iSessionTo != sessions.end())
            {
                iSessionTo->second->MessageAdd(m);
            }
            else if (m.GetAddr() == MR_ALL)
            {
                for (auto& [id, session] : sessions)
                {
                    if (id != m.GetFrom())
                        session->MessageAdd(m);
                }
            }
        }
        break;
    }
    }
}

void Server()
{
    AfxSocketInit();
    CSocket Server;
    Server.Create(12345);
    printf("Server started\n");
    thread t1(CheckIfUserIsInactive);
    t1.detach();

    for (int i = 0; i < 3; i++)
      LaunchClient();

    while (true)
    {
        if (!Server.Listen())
            break;
        CSocket s;
        Server.Accept(s);
        thread t(ClientProcessing, s.Detach());
        t.detach();
    }
    Server.Close();
    printf("Server stoped");
}



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
            Server();
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
