#TODO add credits for code snippets
# https://medium.com/@juanrosario38/how-to-use-pythons-imaplib-to-check-for-new-emails-continuously-b0c6780d796d

from email import policy
from email.header import decode_header
from email.parser import BytesParser
import sys
import re
from termcolor import colored
from itertools import chain
import email
import imaplib
from bs4 import BeautifulSoup as bs
from get_attach import extract_file
from main import DEBUG
from keyring import get_password

##connection handling



###CREDS
IMAP_HOST = get_password("Email Scanner Creds", "IMAP_HOST")
IMAP_PORT = get_password("Email Scanner Creds", "IMAP_PORT")
USER_EMAIL = get_password("Email Scanner Creds", "USER_EMAIL")
USER_PASSWORD = get_password("Email Scanner Creds", "USER_PASSWORD")
APP_PASSWORD = get_password("Email Scanner Creds", "APP_PASSWORD")


stop=False
criteria = {}
uid_max = 0

# number of top emails to fetch

def extract_links_from_body(body):
    # Find all URLs in the email body
    links = re.findall(r'https?://\S+', body)
    return links

## 
def search_string(uid_max, criteria):
    c = list(map(lambda t: (t[0], '"'+str(t[1])+'"'), criteria.items())) + [('UID', '%d:*' % (uid_max+1))]
    return '(%s)' % ' '.join(chain(*c))


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)





try:
    print(colored("🔧 Configuration Details:", "cyan"))
    print(colored(f"IMAP Host     : {IMAP_HOST}", "cyan"))
    print(colored(f"IMAP Port     : {IMAP_PORT}", "cyan"))
    print(colored(f"User Email    : {USER_EMAIL}", "cyan"))
    print(colored(f"User Password : {"*"*len(USER_PASSWORD)}", "cyan"))
    print(colored(f"App Password  : {"*"*len(APP_PASSWORD)}", "cyan"))

    print(colored("\n🔗 Establishing connection to the server...", "yellow"))

    if int(IMAP_PORT) == 993:
        imap = imaplib.IMAP4_SSL(IMAP_HOST, IMAP_PORT)
    else:
        imap = imaplib.IMAP4(IMAP_HOST, IMAP_PORT)
    print(colored("✅ Connection successful!", "green"))
    
    print(colored("🔐 Logging in with provided credentials...", "yellow"))
    password = USER_PASSWORD if USER_PASSWORD else APP_PASSWORD
    imap.login(USER_EMAIL, password)
    print(colored("✅ logged in successfully!", "green"))
    print(colored("📥 Selecting inbox in read-only mode...", "yellow"))
    imap.select('inbox', readonly=True)
except Exception as e:
    print(colored(f"❌ An error occurred: {str(e)}", "red"))

new_email=False
while not stop:
    ##getting uids of emails and success code
    result, data = imap.uid('search', None, search_string(uid_max, criteria))
    uids = [int(s) for s in data[0].split()]
    ## loading max_id key
    from save_last_email_uid import get_last_email_uid
    last_email_uid = int(get_last_email_uid())
    if last_email_uid is None:
        stop=True
        print("last_email_uid is missing")

    #if uids[-1] > data["max_uid"]: # for the prod
    if last_email_uid+1 > last_email_uid: ##for testing
        new_email=True
        result, data = imap.uid('fetch', str(uids[-1]), '(RFC822)')
        msg = email.message_from_bytes(data[0][1])

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or "utf-8")

        from_ = msg.get("From")
        to_ = msg.get("To")
        if DEBUG:
            print(f"Subject: {subject}")
            print(f"From: {from_}")
            print(f"To: {to_}")
        

        # Parse the email using the BytesParser and default policy
        raw_bytes = data[0][1]
        msg = BytesParser(policy=policy.default).parsebytes(raw_bytes)

        # Extract the body
        body = None
        #TODO parse only text msg for both text/plain text/html
        ### https://gist.github.com/sdkn104/45a7451558744a9f191f587e4b61f46

        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == 'text/html':
                    body = part.get_payload(decode=True).decode(part.get_content_charset())
                elif content_type == 'text/plain':
                    body = part.get_payload(decode=True).decode(part.get_content_charset())
        else:
            # Single part email
            content_type = msg.get_content_type()
            if content_type == 'text/html':
                body = msg.get_payload(decode=True).decode(msg.get_content_charset())
            elif content_type == 'text/plain':
                body = msg.get_payload(decode=True).decode(msg.get_content_charset())

        
        if new_email:
            soup = bs(body, 'html.parser')
            body = soup.get_text(separator=' ', strip=True)
            links = extract_links_from_body(body)
            if DEBUG:
                print("Message:\n", body)
                print("links:",links)
            if DEBUG: #if just test demo stop when retireiving an email otherwise keep running
                stop=True 

        status, filepath = extract_file(str(uids[-1]))
        if status==1:
            print(f"attachement was downloaded:{filepath}")
            print("="*30)
        else:
            print("="*30)
            print("no attachements found:")

        ### updateing  max_id value
        from save_last_email_uid import update_last_email_uid
        update_last_email_uid(str(uids[-1]))


        try:
            from phishy_emails_detector import test_emails
            import art
            print(art.text2art("PHISHING-DETECTOR"),"\n","by oussama mejdoubi\nBUG REPORT->\tLINKEDIN:https://github.com/sam99235/PHISHING_DETECTOR_AI/issues")
            stop=True
            test_emails(email=body,subject=subject,links=links,sender_email=from_)
            sys.exit(0)
        except Exception as e:
            stop=True
            print(f"an unexpcted error has occured{e}")
        # your original code starts here

#TODO
#adjust the program to be costumizable using argparsing and and get the user inputs

#using asycn comm check for new msg unless we get a notification from the imap srv
''''The code you provided seems to be a workaround for implementing a polling mechanism instead of using the IDLE feature. While this approach can work, there are some considerations to keep in mind:
Resource Usage: Polling can lead to higher resource usage because the script repeatedly queries the server, even when there are no new messages. IDLE mode is designed to be more efficient as it waits for the server to push updates when new messages arrive.
Latency: Polling introduces latency, especially if the polling interval is not frequent. IDLE mode allows for near real-time updates.
Email Server Limitations: Some email servers may limit the frequency of polling requests to prevent abuse. Check the documentation or terms of service for your email provider to ensure you are not violating any policies.
If your use case allows for polling and the resource usage is acceptable, the provided code should work. However, if you have the option to use an asynchronous library like aioimaplib or imaplib2 that supports IDLE, it would be a more efficient solution.'''
