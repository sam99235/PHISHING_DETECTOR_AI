import requests,os
from typing import Union

####API TO CHECK EMAIL reputation




# Should be treated like an environment variable and secret.
API_KEY = os.getenv('EMAIL_SCANNER_API_KEY')


class Validate(object):
    """
    Class for interacting with the IPQualityScore API.

    Attributes:
        key (str): Your IPQS API key.
        format (str): The format of the response. Default is 'json', but you can also use 'xml'.
        base_url (str): The base URL for the IPQS API.

    Methods:
        email_validation_api(email: str, timeout: int = 1, fast: str = 'false', abuse_strictness: int = 0) -> str:
            Returns the response from the IPQS Email Validation API.
    """

    key = None
    format = None
    base_url = None

    def __init__(self, key, format="json") -> None:
        self.key = key
        self.format = format
        self.base_url = f"https://www.ipqualityscore.com/api/{self.format}/"

    def email_validation_api(self, email: str, timeout: int = 7, fast: str = 'false', abuse_strictness: int = 0) -> str:
        """
        Returns the response from the IPQS Email Validation API.

        Args:
            email (str):
                The email you wish to validate.
            timeout (int):
                Set the maximum number of seconds to wait for a reply from an email service provider.
                If speed is not a concern or you want higher accuracy we recommend setting this in the 20 - 40 second range in some cases.
                Any results which experience a connection timeout will return the "timed_out" variable as true. Default value is 7 seconds.
            fast (str):
                If speed is your major concern set this to true, but results will be less accurate.
            abuse_strictness (int):
                Adjusts abusive email patterns and detection rates higher levels may cause false-positives (0 - 2).

        Returns:
            str: The response from the IPQS Email Validation API.
        """

        url = f"{self.base_url}email/{self.key}/{email}"

        params = {
            "timeout": timeout,
            "fast": fast,
            "abuse_strictness": abuse_strictness
        }

        response = requests.get(url, params=params)
        return response.json()

##params https://www.ipqualityscore.com/documentation/email-validation-api/response-parameters

def check_email(email):
    v = Validate(API_KEY)
    data = v.email_validation_api(email)

    if data["success"]:
        # print(data["disposable"])  #bool true if suspected
        # print(f"risky_tld: {data['risky_tld']}") #bool 
        # print(f"fraud_score: {data['fraud_score']}")  #Fraud Scores >= 75 are suspicious 
        # print(f"recent_abuse: {data['recent_abuse']}") # bool
        # print(f"honeypot: {data['honeypot']}") # bool
        
        disposable = data["disposable"]
        risky_tld = data["risky_tld"]
        fraud_score = data["fraud_score"]
        recent_abuse = data["recent_abuse"]
        honeypot = data["honeypot"]
        if (disposable or recent_abuse or honeypot or risky_tld) and fraud_score >= 75:
            return True 
        else:
            return False
        