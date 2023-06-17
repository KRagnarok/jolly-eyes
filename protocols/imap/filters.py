import datetime
from typing import Optional

from ..basic.filters import * 
from .imap_tool.imap import *

class IMAPEmailSubjectFilter(BasicEmailSubjectFilter):

    def __init__(self, options: Optional[dict], subject: str) -> None:
        super().__init__(options, subject)

    def get_filter_func(self):
        return f"(SUBJECT {self._subject})" 

class IMAPEmailDateFilter(BasicEmailDateFilter):

    def __init__(self, options: Optional[dict], start_date: datetime.datetime, end_date: datetime.datetime) -> None:
        super().__init__(options, start_date, end_date)
        if self._start_date == None and self._end_date == None:
            raise Exception("At least one date should be specified")
        if self._start_date == None and self._is_exact:
            raise Exception("Start time should be provided if exact time is needed")

        if self._options == None:
            self._options = {}

        self._is_exact = self._options.get("is_start_date_exact", False)
        self._date_format = self._options.get("date_format", "%d-%b-%Y")
    
    def get_filter_func(self):
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

class IMAPEmailAuthorFilter(BasicEmailAuthorFilter):

    def __init__(self, options: Optional[dict], author: str) -> None:
        super().__init__(options, author)

    def get_filter_func(self):
        return f"(FROM {self._author})"

class IMAPEmailUnreadFilter(BasicEmailUnreadFilter):

    def __init__(self, options: Optional[dict]) -> None:
        super().__init__(options)

    def get_filter_func(self):
        return "(UNSEEN)"


