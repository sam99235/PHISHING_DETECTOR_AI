import shutil
import argparse,getpass, json, sys,os
from keyring import get_password,delete_password
import keyring
from rich_argparse import RichHelpFormatter
from argparse import ArgumentTypeError
from creds_mgr import load_env_vars, save_env_vars
import subprocess
import sys
import os
import ctypes

default_imap_servers = {"1": {"Gmail": {"address": "imap.gmail.com", "port": 993}}, "2": {"Outlook": {"address": "imap-mail.outlook.com", "port": 993}}, "3": {"Office365": {"address": "outlook.office365.com", "port": 993}}, "4": {"Yahoo-Mail": {"address": "imap.mail.yahoo.com", "port": 993}}, "5": {"Yahoo-Mail-Plus": {"address": "plus.imap.mail.yahoo.com", "port": 993}}, "6": {"Zoho-Mail": {"address": "imap.zoho.com", "port": 993}}}

config_file = "imap_servers.json"
required_env_vars = ["IMAP_HOST", "IMAP_PORT", "USER_EMAIL", "USER_PASSWORD", "APP_PASSWORD"]



class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        # Custom check for users typing values after store_true flags
        for flag in ['--user_password', '--app_password']:
            if flag in sys.argv:
                idx = sys.argv.index(flag)
                if idx + 1 < len(sys.argv):
                    next_arg = sys.argv[idx + 1]
                    if not next_arg.startswith("-"):
                        print(f"❌ Error: The {flag} flag does not take a value. Use it without arguments and hit enter.")
                        sys.exit(2)
        # Otherwise, show normal error
        print(f"❌ Error: {message}")
        sys.exit(2)



parser = CustomArgumentParser(
    description='[bold cyan]Email Graber Tool[bold cyan]',
    usage='1): %(prog)s --imap_server Gmail --email username@gmail.com --user_password\n'\
    '       2): %(prog)s --imap_server Outlook --email username@outlook.com --app_password\n    ' \
    '   3): %(prog)s add_new --costume_name firbomail --imap_server imap.firbo.com --imap_port 933\n' \
    "       4): %(prog)s -runbg OR --run_in_background\n"\
    '       5): %(prog)s -rmvbg OR --remove_background\n'\
    '       HINT: imap servers config file {}'.format(os.path.abspath(config_file))
    ,formatter_class=RichHelpFormatter)

#creating new config file if doesn't exist
if not os.path.exists(config_file):
    print("file is missing\tcreating a new one.....")
    with open(config_file, 'w') as f:
        json.dump(default_imap_servers,f)
    ##printing service address and port

#available choices 
with open(config_file, "r") as f:
            data = json.load(f)
choices = [choice for sub_dict in data.values() for choice in sub_dict.keys()]

#choose ur imap server from availbale options
parser.add_argument('-is','--imap_server',choices=choices, help='choose your imap service above')
parser.add_argument('-e','--email', help='enter your email')
parser.add_argument('--user_password', action='store_true',help='enter your password')
parser.add_argument('--app_password',action='store_true',help='enter your application password')
parser.add_argument('-ss', '--start_scanner', action='store_true', help='luanch email scanner in DEBUGGING MODE')
parser.add_argument('-runbg', '--run_in_background',action='store_true', help='Run the Email Scanner in the background at logon')
parser.add_argument('-rmvbg', '--remove_background',action='store_true', help='Remove the Email Scanner from the background')
parser.add_argument('-ssbg', '--start_scanner_bg', action='store_true', help='luanch email scanner in the background')
parser.add_argument('-rmvc', '--remove_creds', action='store_true', help='remove your credentials')
parser.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity.')
#add costume imap server
subparsers = parser.add_subparsers(dest='command')
parser_add = subparsers.add_parser('add_new',help='Add a new imap server')
parser_add.add_argument('-cn','--costume_name', help='enter a costume name')
parser_add.add_argument('-is','--imap_server',help='enter the imap server address')
parser_add.add_argument('-iport','--imap_port', help='enter the imap server port')


#optionnal args
parser_add.add_argument('-v', '--verbose', action='store_true', help='Increase output verbosity.')

args = parser.parse_args()

#show help by if no args are passed
if len(sys.argv) == 1:
    parser.print_help()
    sys.exit(0)

all_creds = 0 #1->imap_serv,2->user email,3user|app_password

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin(task_name="",action=""):
    script = os.path.abspath(sys.argv[0])
    params = ' '.join([f'"{arg}"' for arg in sys.argv[1:]])
    if len(params)>0:
        result = ctypes.windll.shell32.ShellExecuteW(
                None,        # hwnd
                "runas",     # Operation
                sys.executable,  # Executable (python.exe)
                f'"{script}" {params}',  # Parameters
                None,        # Directory
                1            # Show window
            )

        if result <= 32:
            print(f"[✗] Failed to elevate privileges (ShellExecuteW returned {result})")
            return False
        else:
            if action==1:
                print(f"[✓] Your {task_name} has been added successfully")
            if action==0:
                print(f"[✓] Your {task_name} has been deleted successfully")
            if action==2:
                print(f"[✓] Your {task_name} exists")

def schedule_task(program_path, task_name):
    program_path = os.path.abspath(program_path)
    # Try to find pythonw.exe for silent background execution
    pythonw_path = shutil.which("pythonw") or shutil.which("pythonw.exe")
    if pythonw_path:
        args = f'"{pythonw_path}" "{program_path}"'
    else:
        # Fallback to normal python
        python_path = shutil.which("python") or shutil.which("python.exe")
        if python_path:
            args = f'{pythonw_path} {program_path}'

        else:
            # No interpreter found
            print("[✗] Python interpreter not found.")
            return


    command = f'schtasks /Create /F /TN "{task_name}" /TR "{args} -ssbg" /SC MINUTE /MO 1 /RL HIGHEST '

    result = subprocess.run(command, shell=True)
    if result.returncode == 0:
        print(f"[✓] Task '{task_name}' scheduled successfully.")
    else:
        print("[✗] Failed to schedule task. Try running as administrator.")


# Import the functions into your code


def remove_task(task_name):
    command = f'schtasks /Delete /TN "{task_name}" /F'
    result = subprocess.run(command, shell=True)
    if result.returncode == 0:
        print(f"[✓] Task '{task_name}' removed.")
    else:
        print("[✗] Failed to remove task. Does it exist?")




if args.run_in_background:
    program_path = sys.argv[0]
    if not is_admin():
        print("[-] Not running as admin. Attempting to relaunch...")
        run_as_admin(task_name="Email Scanner",action=1) # if action is run in background
        sys.exit(0)
    print("[+] Running as administrator.")
    if not os.path.exists(program_path):
        print(f"[✗] File does not exist: {program_path}")
        sys.exit(1)
    schedule_task(program_path, task_name="Email Scanner")

if args.remove_background:
    if not is_admin():
        print("[-] Not running as admin. Attempting to relaunch...")
        run_as_admin(task_name="Email Scanner",action=0) #if action is remove background
        sys.exit(0)
    print("[+] Running as administrator.")
    remove_task(task_name="Email Scanner")


##used for get_new_email and get_attach files
IMAP_HOST = ''
IMAP_PORT = 0 
USER_EMAIL = ''
USER_PASSWORD = ''
APP_PASSWORD = ''
DEBUG=False


env_vars = {
                        'IMAP_HOST': IMAP_HOST,
                        'IMAP_PORT': IMAP_PORT,
                        'USER_EMAIL': USER_EMAIL,
                        'USER_PASSWORD': USER_PASSWORD,
                        'APP_PASSWORD': APP_PASSWORD
                    }
def check_creds():
        # Check if all required environment variables exist
        global env_vars,IMAP_HOST,IMAP_PORT,USER_EMAIL,USER_PASSWORD,APP_PASSWORD
        
        if load_env_vars(env_vars.keys()):
                IMAP_HOST = get_password("Email Scanner Creds", "IMAP_HOST")
                IMAP_PORT = get_password("Email Scanner Creds", "IMAP_PORT")
                USER_EMAIL = get_password("Email Scanner Creds", "USER_EMAIL")
                USER_PASSWORD = get_password("Email Scanner Creds", "USER_PASSWORD")
                APP_PASSWORD = get_password("Email Scanner Creds", "APP_PASSWORD")
                if args.start_scanner:
                    global DEBUG
                    DEBUG=True
                    try:
                        import get_new_email # runs main logic
                        # sys.exit(0)  # Skip argparse and other setup
                    except Exception as e:
                        print("an Error has occured:\n{e}")
                if args.start_scanner_bg:  #run the scanner in the background
                    cmd = 'schtasks /Query /TN "Email Scanner"'
                    result = subprocess.run(cmd, shell=True)
                    if result.returncode==0 or 1: ## this is prone to privele errors
                        try:
                            import get_new_email # runs main logic
                        except Exception as e:
                            print(f"An Error has occured:\n{e}")
                    else:
                        print("Run in the background first")
        else:
            print("⚠️  NOTE: Your creds are missing, Try to enter your creds first")
            try:
                user_password = ""  # define default values
                app_password = ""
                if all([args.imap_server,args.email]):
                    globals()["all_creds"]+=1 #for email\
                    if args.verbose:
                        print("valditing your inputs")
                with open(config_file, "r") as f:
                    data = json.load(f)
                for index,choice in zip(data.keys(),choices):
                    if args.imap_server==choice:
                            IMAP_HOST=data[index][choice]["address"]
                            IMAP_PORT=data[index][choice]["port"]
                            globals()["all_creds"]+=1 #for imap server
                if args.user_password:
                    user_password = getpass.getpass(prompt="Enter your email password (hidden): ")
                    if user_password:
                        globals()["all_creds"]+=1 #for user pass
                        print("Password received (hidden for security)")
                # Secure app assword prompt
                if args.app_password:
                    app_password = getpass.getpass(prompt="Enter your application password (hidden): ")
                    if app_password:
                        globals()["all_creds"]+=1 #for app pass
                        print("App Password received (hidden for security)")
                    if args.verbose and len(app_password)>0:
                            print("success")
                if all_creds==3:
                    env_vars = {
                                    'IMAP_HOST': IMAP_HOST,
                                    'IMAP_PORT': IMAP_PORT,
                                    'USER_EMAIL': args.email,
                                    'USER_PASSWORD': user_password,
                                    'APP_PASSWORD': app_password
                                }
                    save_env_vars(env_vars)
                    return True
            except ArgumentTypeError as e:
                print("your inputs are not valid\tcheck usage examples")
                return False
check_creds()

if args.remove_creds:
        try:
            for key in env_vars.keys():
                delete_password("Email Scanner Creds",key)
                print("Your creds has been deleted")
        except keyring.errors.PasswordDeleteError:
            print("Your creds already has been deleted")

if args.command=='add_new':
    if args.verbose:
        print('adding costume imap server')
    if args.imap_server is not None and args.imap_port  is not None:
        import json
        #loading keys 
        with open(config_file, "r") as f:
            data = json.load(f)
        keys = [int(k) for k in data.keys()]
        new_key = max(keys) + 1  # Find the next numeric key
        data[new_key]= {
        args.costume_name: {
            "address": args.imap_server,
            "port": args.imap_port
        }}
        ##saving changes
        with open(config_file, "w") as f:
            json.dump(data,f)
            f.close()
            print(f"success")
            if args.verbose:
                print('costume imap server has been added successfully')
    else:
        print("please add params ,check usage examples")


#TODO 
#to fix scheduled task doesn't run automtically
#logging errors|bugs in every step
#raising exceptions