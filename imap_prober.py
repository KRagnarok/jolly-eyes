from typing import Optional

from exchangelib.ewsdatetime import datetime
from email_prober import BasicEmailProber,BasicEmailHolder , EmailAccountInfo, BasicEmailFilter
from imap_tool.imap import *

### Filters ###
class BasicIMAPEmailFilter(BasicEmailFilter):

    def __init__(self) -> None:
        super().__init__()

    def get_filtered_emails(self, all_emails):
        return super().get_filtered_emails(all_emails)

    def get_query_string(self):
        raise NotImplementedError()

class IMAPEmailSubjectFilter(BasicIMAPEmailFilter):

    def __init__(self, subject) -> None:
        self._subject = subject
        
    def get_filtered_emails(self, all_emails):
        raise NotImplementedError()

    def get_query_string(self):
        return f"(SUBJECT {self._subject})" 

class IMAPEmailDateFilter(BasicIMAPEmailFilter):

    def __init__(self, start_date: Optional[datetime.datetime], 
                 end_date: Optional[datetime.datetime], is_start_date_exact: bool = False,
                 date_format: str = "%d-%b-%Y") -> None:
        self._start_date = start_date 
        self._end_date = end_date 
        self._is_exact = is_start_date_exact
        if self._start_date == None and self._end_date == None:
            raise Exception("At least one date should be specified")
        if self._start_date == None and self._is_exact:
            raise Exception("Start time should be provided if exact time is needed")

        self._date_format = date_format

    def get_filtered_emails(self, all_emails):
        raise NotImplementedError()
    
    def get_query_string(self):
        query = "("
        if self._is_exact and self._start_date != None:
            query = f"(ON {self._start_date.strftime(self._date_format)})"
            return query

        if self._start_date != None:
            query += f"SINCE {self._start_date.strftime(self._date_format)} "

        if self._end_date != None:
            query += f"BEFORE {self._end_date.strftime(self._date_format)} "
        
        query += ")"
        return query

class IMAPEmailAuthorFilter(BasicIMAPEmailFilter):

    def __init__(self, author: str) -> None:
        self._author = author
    
    def get_filtered_emails(self, all_emails):
        raise NotImplementedError()

    def get_query_string(self):
        return f"(FROM {self._author})"

### Holder ###
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
    
class IMAPEmailProber(BasicEmailProber):

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
