from dataclasses import dataclass
from imaplib import IMAP4_SSL
from typing import Optional
import email
from email.header import decode_header


class IMAP4Email():

    def __init__(self, msg) -> None:
        self._msg = msg

    def _decode_header(self, header_string):
        try:
            value, encoding = decode_header(header_string)[0]
            if isinstance(value, bytes) and encoding != None:
                return value.decode(encoding)
            elif encoding == None:
                return value.decode()
            else:
                return value
        except Exception: # fallback: return as is
            return header_string

    def parse_email_headers(self):
        for response in self._msg:
            if isinstance(response, tuple):
                msg = email.message_from_bytes(response[1])
                self.subject = self._decode_header(msg["Subject"]) 
                self.author = self._decode_header(msg["From"]) 
                self.to = self._decode_header(msg["To"]) 
                self.date = self._decode_header(msg["Date"]) 

    def parse_email_content(self):
        raise NotImplementedError()

       
class IMAP4EmailIterator():

    def __init__(self, messages: list, imap_login, is_search: bool) -> None:
        # We do an optimized way here. However, the optimized way is to differntiate between search and select.
        self._messages = messages[0].decode().split()
        self._imap_login = imap_login
        if not is_search:
            self._messages = [i for i in self._messages]

        self._messages.reverse()            
        self._total_messages = len(self._messages)
        self._cnt = self._total_messages

    def __next__(self):
        if self._cnt <= 0:
            raise StopIteration

        res, msg = self._imap_login.fetch(self._messages[self._cnt - 1], "(RFC822)")
        self._cnt -= 1
        
        email = IMAP4Email(msg)
        email.parse_email_headers()

        # TODO: parse content
        return email

    def __iter__(self):
        return self
        

class IMAP4EmailContainer():


    def __init__(self, imap_login, mailbox: str) -> None:
        self._imap_login = imap_login
        status, self._messages = self._imap_login.select(mailbox)
        # Apparently, when we do select, imaplib just returns the last email ID, which means we should iterate by ourselves.
        # On the other hand, when we do a search, imaplib returns all the emails that match the specified query, so it is now a list rather than a number. 
        # Thus, we need a way to differentiate between these two things so that we can iterate over them.
        self._is_search = False


    def filter_emails(self, query: str):
        typ, self._messages = self._imap_login.search(None, query)
        self._is_search = True

    @property
    def count(self):
        return len(self._messages[0].decode().split())

    def __iter__(self):
        return IMAP4EmailIterator(self._messages, self._imap_login, self._is_search)
        

@dataclass
class EmailAccountAuthInfo():
    email_address: str
    username: str
    password: str
    server_address: str
    server_port: Optional[int]

class IMAP4SSLAuthenticationWraper():

    def __init__(self, auth_info: EmailAccountAuthInfo) -> None:
        self._auth_info = auth_info
        self._list_of_available_mailboxes = {}


    def login(self):
        if self._auth_info.server_port == None or (self._auth_info.server_port < 0 or self._auth_info.server_port > 65535):
            self._imap_login = IMAP4_SSL(self._auth_info.server_address)
        else:
            self._imap_login = IMAP4_SSL(self._auth_info.server_address, self._auth_info.server_port)
        self._imap_login.login(self._auth_info.username, self._auth_info.password)

    def logout(self):
        self._imap_login.close()
        self._imap_login.logout()

    def update_list_of_mailboxes(self):
        self._list_of_available_mailboxes = self._imap_login.list()

    def mailbox(self, mail_box_name: str = "INBOX"):
        return IMAP4EmailContainer(self._imap_login, mail_box_name)
        
        
