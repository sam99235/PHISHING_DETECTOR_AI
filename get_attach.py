
####
##this script saves emails attachements
###
import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv
load_dotenv()


# account credentials
# username = ""
# password = ""
# # use your email provider's IMAP server, you can look for your provider's IMAP server on Google
# # or check this page: https://www.systoolsgroup.com/imap/
# # for office 365, it's this:
# imap_server = "imap.gmail.com"

IMAP_HOST = os.getenv("IMAP_HOST")
IMAP_PORT = os.getenv("IMAP_PORT")
USER_EMAIL = os.getenv("USER_EMAIL")
USER_PASSWORD = os.getenv("USER_PASSWORD")
APP_PASSWORD = os.getenv("APP_PASSWORD")

def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)

# create an IMAP4 class with SSL
try:
    if int(IMAP_PORT) == 993:
        imap = imaplib.IMAP4_SSL(IMAP_HOST, int(IMAP_PORT))
    else:
        imap = imaplib.IMAP4(IMAP_HOST, int(IMAP_PORT))
    password = USER_PASSWORD if USER_PASSWORD else APP_PASSWORD
    imap.login(USER_EMAIL, password)
    print("Connection successful!")
    status, messages = imap.select("INBOX")
    # number of top emails to fetch
    N = 1
    # total number of emails
    messages = int(messages[0])
except Exception as e:
    print(f"Error connecting to the server: {e}")


#TODO IT DOESN'T DOWNLAOD THE LAST ATTACHMENT
def extract_file(uid):

   # for i in range(messages, messages-N, -1):
        # fetch the email message by ID
        res_,msg = imap.uid('fetch', str(uid), '(RFC822)')
        #res, msg = imap.fetch(str(i), "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_bytes(response[1])
                # decode the email subject
                subject, encoding = decode_header(msg["Subject"])[0]
                if isinstance(subject, bytes):
                    # if it's a bytes, decode to str
                    subject = subject.decode(encoding)
                # if the email message is multipart
                if msg.is_multipart():
                    # iterate over email parts
                    for part in msg.walk():
                        # extract content type of email
                        content_type = part.get_content_type()
                        content_disposition = str(part.get("Content-Disposition"))
                        try:
                            # get the email body
                            body = part.get_payload(decode=True).decode()
                        except:
                            pass
                        if content_type == "text/plain" and "attachment" not in content_disposition:
                            # print text/plain emails and skip attachments
                            #print("no attachments found")
                            _ = 'this condition needs to adjusted'
                        elif "attachment" in content_disposition:
                            # download attachment
                            filename = part.get_filename()
                            if filename:
                                folder_name = clean(subject)
                                if not os.path.isdir(folder_name):
                                    # make a folder for this email (named after the subject)
                                    os.mkdir(folder_name)
                                filepath = os.path.join(folder_name, filename)
                                # download attachment and save it
                                open(filepath, "wb").write(part.get_payload(decode=True))
                                full_path = os.path.abspath(filepath)
                                return 1,full_path
                print("="*100)
        
        
        #TODO THIS RETURN MUST BE TESTED
        return 0,None
    # close the connection and logout

# imap.close()
# imap.logout()