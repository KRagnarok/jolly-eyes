from imap_tool.imap import *
from ..basic.connector import BasicEmailConnector, BasicEmailHolder, EmailAccountInfo
from .filters import BasicIMAPEmailFilter

class IMAPEmailHolder(BasicEmailHolder):

    def __init__(self, all_emails) -> None:
        super().__init__(all_emails)
        self._queries = []

    def apply_filter(self, filter : BasicIMAPEmailFilter):
        self._queries.append(filter.get_query_string())
    
    def get_emails(self):
        if len(self._queries) == 0:
            return self._all_available_emails

        query = self._queries[0]

        for i in range(1, len(self._queries)):
            query += " AND "
            query += self._queries[i]

        self._all_available_emails.filter_emails(query)

        return self._all_available_emails
    
class IMAPEmailConnector(BasicEmailConnector):

    def __init__(self, email_acc_info : EmailAccountInfo):
        self._email_acc_info = email_acc_info 
        self._is_connected = False

    def connect_and_auth(self):
        self._imap_login = IMAP4SSLAuthenticationWraper(
                EmailAccountAuthInfo(
                    email_address=self._email_acc_info.email_address,
                    username=self._email_acc_info.username,
                    password=self._email_acc_info.password,
                    server_address=self._email_acc_info.server_address,
                    server_port=self._email_acc_info.server_port
                    )
                )
        self._imap_login.login()
        inbox = self._imap_login.mailbox()

    def get_all_emails(self):
        return IMAPEmailHolder(self._imap_login.mailbox())
