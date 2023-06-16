from typing import Optional
import datetime

from exchangelib import Q
from ..basic.connector import BasicEmailFilter

class BasicExchangeFilter(BasicEmailFilter):

    def __init__(self) -> None:
        super().__init__()

    def get_filtered_emails(self, all_emails):
        return super().get_filtered_emails(all_emails)
    
    def get_query_function(self):
        raise NotImplementedError()
  
class ExchangeEmailAuthorFilter(BasicExchangeFilter):

    def __init__(self, author: str, contains: bool = False, like: bool = False) -> None:
        self._author = author
        self._contains = contains
        self._like = like
    
    def get_filtered_emails(self, all_emails):
        raise NotImplementedError()

    def get_query_function(self):
        if self._contains:
            if self._like:
                return Q(sender__icontains=self._author)
            return Q(sender__contains=self._author)

        if self._like:
            return Q(sender__iexact=self._author)
        return Q(sender=self._author)

class ExchangeEmailDateFilter(BasicExchangeFilter):

    def __init__(self, start_date: Optional[datetime.datetime], 
                 end_date: Optional[datetime.datetime]) -> None:
        self._start_date = start_date 
        self._end_date = end_date 
        if self._start_date == None and self._end_date == None:
            raise Exception("At least one date should be specified")

    def get_filtered_emails(self, all_emails):
        raise NotImplementedError()

    def get_query_function(self):
        query = None
        if self._start_date != None:
            query = Q(start__gte=self._start_date)

        if self._end_date != None:
            if query != None:
                query = query & Q(end__lte=self._end_date)
            else:
                query = Q(end__lte=self._end_date)
        
        return query
        
class ExchangeEmailSubjectFilter(BasicExchangeFilter):
    def __init__(self, subject: str, contains: bool = False, like: bool = False) -> None:
        self._subject = subject
        self._contains = contains
        self._like = like

    def get_filtered_emails(self, all_emails):
        raise NotImplementedError()

    def get_query_function(self):
        if self._contains:
            if self._like:
                return Q(subject__icontains=self._subject)
            return Q(subject__contains=self._subject)

        if self._like:
            return Q(subject__iexact=self._subject)
        return Q(subject=self._subject)
 
