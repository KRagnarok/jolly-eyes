from typing import Optional
from email_prober import EmailProber, EmailAccountInfo, EmailFilter
from exchangelib import DELEGATE, Account, Configuration, Credentials


class ExchangeEmailProber(EmailProber):

    def __init__(self, email_acc_info : EmailAccountInfo):
        self._email_acc_info = email_acc_info 
        self._is_connected = False

    def connect_and_auth(self):
        self._credentials = Credentials(
                username = self._email_acc_info.username,
                password = self._email_acc_info.password
        )
        self._config = Configuration(
                server = self._email_acc_info.server_address,
                credentials = self._credentials
        )
        self._account = Account(
                primary_smtp_address = self._email_acc_info.email_address,
                config = self._config,
                autodiscover = False,
                access_type = DELEGATE
        )
        self._is_connected = True

    def get_all_emails(self, filter: Optional[EmailFilter] = None):
        return self._account.inbox.all()

    def get_unread_emails(self, filter: Optional[EmailFilter] = None):
       unread_emails =  self._account.inbox.filter(is_read=False)
        if filter == None:
            return unread_emails
        
        return unread_emails 
 
