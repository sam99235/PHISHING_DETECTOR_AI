# env_utils.py
import keyring
import os

def save_env_vars(vars_dict: dict, service_name: str ="Email Scanner Creds"):
    """
    Save environment variables securely using keyring.
    Keys become usernames in the credential store.
    """
    for key, value in vars_dict.items():
        keyring.set_password(service_name, key, value)
    print("✅ Credentials saved securely to system keyring.")

def load_env_vars(keys: list, service_name: str = "Email Scanner Creds") -> bool:
    """
    Load environment variables from keyring into os.environ.
    Returns True if all keys were found, False otherwise.
    """
    for key in keys:
        value = keyring.get_password(service_name, key)
        if value is not None:
            os.environ[key] = value
        else:
            return False
    return True
