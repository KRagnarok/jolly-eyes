from typing import Optional
import datetime

from exchangelib import Q
from ..basic.filters import *

class ExchangeEmailAuthorFilter(BasicEmailAuthorFilter):

    def __init__(self, options: Optional[dict], author: str) -> None:
        super().__init__(options, author)
        
        if self._options == None:
            self._options = {}

        self._contains = self._options.get("contains", False)
        self._like = self._options.get("like", False)
            
    def get_filter_func(self):
        if self._contains:
            if self._like:
                return Q(sender__icontains=self._author)
            return Q(sender__contains=self._author)

        if self._like:
            return Q(sender__iexact=self._author)
        return Q(sender=self._author)

class ExchangeEmailDateFilter(BasicEmailDateFilter):

    def __init__(self, options: Optional[dict], start_date: datetime.datetime, end_date: datetime.datetime) -> None:
        super().__init__(options, start_date, end_date)
        if self._start_date == None and self._end_date == None:
            raise Exception("At least one date should be specified")

    def get_filter_func(self):
        query = None
        if self._start_date != None:
            query = Q(start__gte=self._start_date)

        if self._end_date != None:
            if query != None:
                query = query & Q(end__lte=self._end_date)
            else:
                query = Q(end__lte=self._end_date)
        
        return query

class ExchangeEmailSubjectFilter(BasicEmailSubjectFilter):

    def __init__(self, options: Optional[dict], subject: str) -> None:
        super().__init__(options, subject)
        if self._options == None:
            self._options = {}
            
        self._contains = self._options.get("contains", False)
        self._like = self._options.get("like", False) 
            
    def get_filter_func(self):
        if self._contains:
            if self._like:
                return Q(subject__icontains=self._subject)
            return Q(subject__contains=self._subject)

        if self._like:
            return Q(subject__iexact=self._subject)
        return Q(subject=self._subject)

class ExchangeEmailUnreadFilter(BasicEmailUnreadFilter):

    def __init__(self, options: Optional[dict]) -> None:
        super().__init__(options)

    def get_filter_func(self):
        return Q(is_read=False)

