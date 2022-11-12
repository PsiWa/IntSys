using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.StartPanel;

namespace SereginSharpClient
{
    public partial class UsernameForm : Form
    {
        private Form1 formref;
        private ListBox mlbref;
        private ListBox ulbref;
        public UsernameForm(Form1 form1, ref ListBox mlbref,ref ListBox ulbref)
        {
            this.formref = form1;
            this.mlbref = mlbref;
            this.ulbref = ulbref;
            InitializeComponent();
        }

        private void UsernameSendBTN_Click(object sender, EventArgs e)
        {
            if (UsernameTEXT.Text != "")
            {
                var m = Message.send(MessageRecipients.MR_BROKER, MessageTypes.MT_INIT, UsernameTEXT.Text+" "+PassTEXT.Text);
                if (m.GetAction() == MessageTypes.MT_DECLINE)
                {
                    MessageBox.Show("Error");
                    UsernameTEXT.Text = "";
                }
                else
                {
                    Form1.username = UsernameTEXT.Text;
                    formref.Enabled = true;
                    string[] parts = m.GetData().Split(new[] { '\n' });
                    foreach (string part in parts)
                        mlbref.Items.Add(part);
                    mlbref.Items.Add($"server: Hello {UsernameTEXT.Text}!");
                    Thread t = new Thread(() => Form1.ProcessMessages(ref this.formref,ref this.mlbref, ref this.ulbref));
                    t.Start();
                    this.Close();
                }
            }
            else
            {
                MessageBox.Show("Error");
            }
        }
    }
}
