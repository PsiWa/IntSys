namespace SereginSharpClient
{
    partial class UsernameForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
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
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.UsernameSendBTN = new System.Windows.Forms.Button();
            this.UsernameTEXT = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.PassTEXT = new System.Windows.Forms.TextBox();
            this.label2 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // UsernameSendBTN
            // 
            this.UsernameSendBTN.Location = new System.Drawing.Point(12, 135);
            this.UsernameSendBTN.Name = "UsernameSendBTN";
            this.UsernameSendBTN.Size = new System.Drawing.Size(153, 41);
            this.UsernameSendBTN.TabIndex = 0;
            this.UsernameSendBTN.Text = "Send";
            this.UsernameSendBTN.UseVisualStyleBackColor = true;
            this.UsernameSendBTN.Click += new System.EventHandler(this.UsernameSendBTN_Click);
            // 
            // UsernameTEXT
            // 
            this.UsernameTEXT.Location = new System.Drawing.Point(13, 52);
            this.UsernameTEXT.Name = "UsernameTEXT";
            this.UsernameTEXT.Size = new System.Drawing.Size(153, 23);
            this.UsernameTEXT.TabIndex = 1;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Font = new System.Drawing.Font("Segoe UI", 14F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point);
            this.label1.Location = new System.Drawing.Point(12, 24);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(153, 25);
            this.label1.TabIndex = 2;
            this.label1.Text = "Enter UserName:";
            // 
            // PassTEXT
            // 
            this.PassTEXT.Location = new System.Drawing.Point(12, 106);
            this.PassTEXT.Name = "PassTEXT";
            this.PassTEXT.PasswordChar = '*';
            this.PassTEXT.Size = new System.Drawing.Size(153, 23);
            this.PassTEXT.TabIndex = 3;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Font = new System.Drawing.Font("Segoe UI", 14F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point);
            this.label2.Location = new System.Drawing.Point(12, 78);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(144, 25);
            this.label2.TabIndex = 4;
            this.label2.Text = "Enter Password:";
            // 
            // UsernameForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(178, 182);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.PassTEXT);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.UsernameTEXT);
            this.Controls.Add(this.UsernameSendBTN);
            this.Name = "UsernameForm";
            this.Text = "UsernameForm";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private Button UsernameSendBTN;
        private TextBox UsernameTEXT;
        private Label label1;
        private TextBox PassTEXT;
        private Label label2;
    }
}