import subprocess
import sys

def send_email(subject, body, to="yvette.halili@telusinternational.com", from_email="no-reply@yourdomain.com"):
    ssmtp_command = "/usr/sbin/ssmtp"
    
    email_content = """To: {to}
From: {from_email}
MIME-Version: 1.0
Content-Type: text/html; charset=utf-8
Subject: {subject}

Hi DBA Team,<br /><br />
We encountered a bit of a hiccup during the backup process:<br /><br />
<span style="color:red;">{body}</span><br /><br />
Please check <b>susweyak03</b> for more details.<br /><br />

Kind Regards,<br />
Your Backup System
""".format(to=to, from_email=from_email, subject=subject, body=body)
    
    try:
        process = subprocess.Popen(ssmtp_command, stdin=subprocess.PIPE, shell=True)
        process.stdin.write(email_content.encode('utf-8'))
        process.stdin.close()
        process.wait()
    except Exception as e:
        print("Failed to send email: {}".format(e))
        with open('/backup/logs/email_error.log', 'a') as f:
            f.write(str(e) + '\n')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: test_error_backup_email.py <subject> <body>")
        sys.exit(1)

    subject = sys.argv[1]
    body = sys.argv[2]
    send_email(subject, body)
