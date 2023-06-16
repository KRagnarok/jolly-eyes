import datetime
from typing import Optional

from ..basic.connector import BasicEmailFilter
from imap_tool.imap import *

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


