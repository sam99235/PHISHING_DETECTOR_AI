#THIS IS USED TO STORE LAST_EMAIL_UID WHICH'S USED FOR CHECKING NEW EMAILS
import winreg

REG_PATH = r"Software\\Email Scanner"
ROOT_KEY = winreg.HKEY_CURRENT_USER

def save_to_registry(key_name, value, root=ROOT_KEY):
    try:
        key = winreg.CreateKeyEx(root, REG_PATH, 0, winreg.KEY_SET_VALUE)
        
        ##value param is in str 
        winreg.SetValueEx(key, key_name, 0, winreg.REG_SZ, value)
        winreg.CloseKey(key)
    except WindowsError as e:
        print(f"❌ Error saving '{key_name}' to Registry: {e}")

def read_from_registry(key_name, root=ROOT_KEY):
    try:
        key = winreg.OpenKey(root, REG_PATH, 0, winreg.KEY_READ)
        value, _ = winreg.QueryValueEx(key, key_name)
        winreg.CloseKey(key)
        return value
    except FileNotFoundError:
        print(f"⚠️ Registry key '{key_name}' not found.")
        return None
    except WindowsError as e:
        print(f"❌ Error reading '{key_name}' from Registry: {e}")
        return None

def update_last_email_uid(new_uid):
    save_to_registry("last_email_uid", new_uid)

def get_last_email_uid():
    return read_from_registry("last_email_uid")
