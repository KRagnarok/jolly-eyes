from typing import Optional
from email_prober import BasicEmailProber,BasicEmailHolder , EmailAccountInfo, BasicEmailFilter
from imaplib import IMAP4_SSL



### Filters ###
class BasicIMAPEmailFilter(BasicEmailFilter):

    def __init__(self) -> None:
        super().__init__()

    def get_filtered_emails(self, all_emails):
        return super().get_filtered_emails(all_emails)

class IMAPEmailSubjectFilter(BasicIMAPEmailFilter):

    def __init__(self) -> None:
        super().__init__()

    def get_filtered_emails(self, all_emails):
        raise NotImplementedError()

### Holder ###
class IMAPEmailHolder(BasicEmailHolder):

    def __init__(self, all_emails) -> None:
        super().__init__(all_emails)

    def apply_filter(self):
        return super().apply_filter()

    def get_emails(self):
        return super().get_emails()
    
class IMAPEmailProber(BasicEmailProber):

    def __init__(self, email_acc_info : EmailAccountInfo):
        self._email_acc_info = email_acc_info 
        self._is_connected = False

    def connect_and_auth(self):
        self._imap_login = IMAP4_SSL(self._email_acc_info.server_address, self._email_acc_info.server_port)
        self._imap_login.login(self._email_acc_info.username, self._email_acc_info.password)
        
        print(self._imap_login.list())

    def get_all_emails(self):
        pass
