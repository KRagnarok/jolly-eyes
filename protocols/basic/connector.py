from dataclasses import dataclass
from datetime import datetime
from typing import Union

from .filters import BasicEmailFilter

@dataclass
class EmailAccountInfo():
    username: str
    password: str
    email_address: str
    server_address: str
    server_port: int = -1

@dataclass
class EmailInfo():
    sender: str
    receiver: Union[str, None]
    subject: str
    date: datetime

class BasicEmailHolder():

    def __init__(self, all_emails) -> None:
        self._all_available_emails = all_emails

    def apply_filter(self, filter : BasicEmailFilter):
        raise NotImplementedError()

    def get_emails(self):
        raise NotImplementedError()

    def get_standard_email_info(self, email) -> EmailInfo:
        raise NotImplementedError()

    def get_proper_author_name(self, author_name: str, author_email_address: str):
        return f"{author_name} <{author_email_address}>"

class BasicEmailConnector():
    
    def __init__(self, email_acc_info : EmailAccountInfo):
        self._email_acc_info = email_acc_info 
        self._is_connected = False

    def connect_and_auth(self):
        raise NotImplementedError()

    def get_all_emails(self) -> BasicEmailHolder:
        raise NotImplementedError()


