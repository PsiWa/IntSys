using Microsoft.VisualBasic.ApplicationServices;
using System.Runtime.CompilerServices;
using System.Windows.Forms;

namespace SereginSharpClient
{
    public partial class Form1 : Form
    {
        static SortedDictionary<int, string> ActiveUsers = new SortedDictionary<int, string>();
        public static string username;
        static void RefreshActiveUsers(string str, ref ListBox ulb)
        {
            ActiveUsers.Clear();
            string[] buf = str.Split(' ');
            for (int i=0; i<buf.Length-1; i=i+2)
            {
                ActiveUsers.Add(int.Parse(buf[i]), buf[i+1]);
            }
            ulb.Items.Clear();
            ulb.Items.Add("All users");
            foreach (var user in ActiveUsers)
            {
                if (user.Value!=username)
                    ulb.Items.Add($"{user.Value} ({user.Key})");
            }
        }
        public static void ProcessMessages(ref Form1 form,ref ListBox mlb, ref ListBox ulb)
        {
            while (true)
            {
                var m = Message.send(MessageRecipients.MR_BROKER, MessageTypes.MT_REFRESH, ActiveUsers.Count.ToString());
                if (m.GetAction() != MessageTypes.MT_DECLINE)
                {
                    RefreshActiveUsers(m.GetData(),ref ulb);
                }
                m = Message.send(MessageRecipients.MR_BROKER, MessageTypes.MT_GETDATA);
                switch (m.GetAction())
                {
                    case MessageTypes.MT_DATA:
                        mlb.Items.Add($"{ActiveUsers[(int)m.GetFrom()]}: {m.GetData()}");
                        break;
                    case MessageTypes.MT_EXIT:
                        m = Message.send(MessageRecipients.MR_BROKER, MessageTypes.MT_EXIT);
                        form.Close();
                        break;
                    default:
                        Thread.Sleep(1000);
                        break;
                }
            }
        }

        public Form1()
        {
            InitializeComponent();
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            UsersLB.Items.Add("All users");
            Control.CheckForIllegalCrossThreadCalls = false;
            UsernameForm newfom = new UsernameForm(this,ref MessagesLB, ref this.UsersLB);
            newfom.Show();
            this.Enabled = false;
        }

        private void SendBTN_Click(object sender, EventArgs e)
        {
            int recipient = (int)MessageRecipients.MR_ALL;
            var msg = MessageBOX.Text;
            foreach (var user in ActiveUsers)
            {
                if (UsersLB.SelectedItem.ToString().Contains(user.Value))
                {
                    recipient = user.Key;
                    MessagesLB.Items.Add($"You whispered to {user.Value}: {msg}");
                    break;
                }
                MessagesLB.Items.Add($"You: {msg}");
            }
            Message.send((MessageRecipients)recipient, MessageTypes.MT_DATA, (recipient == (int)MessageRecipients.MR_ALL ? "" : "(private) ") + msg);
            MessageBOX.Clear();
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            Message.send(MessageRecipients.MR_BROKER, MessageTypes.MT_EXIT);
        }
    }
}