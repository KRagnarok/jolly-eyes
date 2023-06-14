from datetime import datetime
from typing import Optional
from dataclasses import dataclass

@dataclass
class EmailAccountInfo():
    username: str
    password: str
    email_address: str
    server_address: str
    server_port: int = -1

@dataclass
class EmailBasicInfo():
    author_name: str
    subject: str
    body: str
    time: datetime 
        
class EmailFilter():

    def filter_email(self, email_info : EmailBasicInfo) -> bool:
        raise NotImplementedError()

class EmailProber():
    
    def __init__(self, email_acc_info : EmailAccountInfo):
        self._email_acc_info = email_acc_info 
        self._is_connected = False

    def connect_and_auth(self):
        raise NotImplementedError()

    def get_all_emails(self, filter : Optional[EmailFilter] = None):
        raise NotImplementedError()

    def get_unread_emails(self, filter : Optional[EmailFilter] = None):
        raise NotImplementedError()

    
