import subprocess
import sys

def send_simple_email():
    ssmtp_command = "/usr/sbin/ssmtp"
    
    email_content = """To: yvette.halili@telusinternational.com
From: no-reply@telusinternational.com
Subject: Test Email

This is a simple test email to verify SSMTP functionality.
"""
    
    try:
        with open('/backup/logs/simple_email_content.log', 'w') as f:
            f.write(email_content)
        
        process = subprocess.Popen(ssmtp_command + " yvette.halili@telusinternational.com", stdin=subprocess.PIPE, shell=True)
        process.communicate(input=email_content.encode('utf-8'))
        
        if process.returncode != 0:
            raise Exception("SSMTP process failed with return code {}".format(process.returncode))
        
        print("Simple email sent successfully")
    except Exception as e:
        print("Failed to send simple email: {}".format(e))
        with open('/backup/logs/email_error.log', 'a') as f:
            f.write(str(e) + '\n')

if __name__ == "__main__":
    send_simple_email()
