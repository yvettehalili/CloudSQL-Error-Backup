import subprocess
import sys
import re

EMAIL_SCRIPT_PATH = "/backup/scripts/test_error_backup_email.py"

def sanitize_body(body):
    body = re.sub(r"-u\S+\s", "-u*** ", body)  # Hide username
    body = re.sub(r"-p\S+ ", "-p*** ", body)   # Hide password
    return body

def send_email(subject, body, to="yvette.halili@telusinternational.com", from_email="no-reply@telusinternational.com"):
    ssmtp_command = "/usr/sbin/ssmtp"

    sanitized_body = sanitize_body(body)
    
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
susweyak03
""".format(to=to, from_email=from_email, subject=subject, body=sanitized_body)

    try:
        # Log the email content for debugging
        with open('/backup/logs/email_content.log', 'w') as f:
            f.write(email_content)

        # Use subprocess.Popen without shell=True and pass the recipient correctly
        process = subprocess.Popen([ssmtp_command, to], stdin=subprocess.PIPE)
        process.communicate(input=email_content.encode('utf-8'))

        if process.returncode != 0:
            raise Exception("SSMTP process failed with return code {}".format(process.returncode))

        print("Email sent successfully")
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
    send_email(subject, body, to="yvette.halili@telusinternational.com")
