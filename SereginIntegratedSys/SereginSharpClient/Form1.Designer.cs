namespace SereginSharpClient
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.MessagesLB = new System.Windows.Forms.ListBox();
            this.UsersLB = new System.Windows.Forms.ListBox();
            this.SendBTN = new System.Windows.Forms.Button();
            this.MessageBOX = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // MessagesLB
            // 
            this.MessagesLB.Enabled = false;
            this.MessagesLB.FormattingEnabled = true;
            this.MessagesLB.ItemHeight = 15;
            this.MessagesLB.Location = new System.Drawing.Point(137, 12);
            this.MessagesLB.Name = "MessagesLB";
            this.MessagesLB.Size = new System.Drawing.Size(651, 334);
            this.MessagesLB.TabIndex = 0;

            // 
            // UsersLB
            // 
            this.UsersLB.FormattingEnabled = true;
            this.UsersLB.ItemHeight = 15;
            this.UsersLB.Location = new System.Drawing.Point(11, 12);
            this.UsersLB.Name = "UsersLB";
            this.UsersLB.Size = new System.Drawing.Size(120, 334);
            this.UsersLB.TabIndex = 1;
            // 
            // SendBTN
            // 
            this.SendBTN.Location = new System.Drawing.Point(656, 352);
            this.SendBTN.Name = "SendBTN";
            this.SendBTN.Size = new System.Drawing.Size(132, 23);
            this.SendBTN.TabIndex = 2;
            this.SendBTN.Text = "Send";
            this.SendBTN.UseVisualStyleBackColor = true;
            this.SendBTN.Click += new System.EventHandler(this.SendBTN_Click);
            // 
            // MessageBOX
            // 
            this.MessageBOX.Location = new System.Drawing.Point(137, 352);
            this.MessageBOX.Name = "MessageBOX";
            this.MessageBOX.Size = new System.Drawing.Size(513, 23);
            this.MessageBOX.TabIndex = 3;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(800, 392);
            this.Controls.Add(this.MessageBOX);
            this.Controls.Add(this.SendBTN);
            this.Controls.Add(this.UsersLB);
            this.Controls.Add(this.MessagesLB);
            this.Name = "Form1";
            this.Text = "Form1";
            this.FormClosing += new System.Windows.Forms.FormClosingEventHandler(this.Form1_FormClosing);
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private ListBox MessagesLB;
        private ListBox UsersLB;
        private Button SendBTN;
        private TextBox MessageBOX;
    }
}