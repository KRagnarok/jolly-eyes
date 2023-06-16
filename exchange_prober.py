from typing import Optional
from exchangelib.ewsdatetime import datetime
from email_prober import BasicEmailProber, EmailAccountInfo, BasicEmailHolder, BasicEmailFilter
from exchangelib import DELEGATE, Account, Configuration, Credentials, Q


### Filters ###
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
    
### Holder ###
class ExchangeEmailHolder(BasicEmailHolder):

    def __init__(self, all_emails) -> None:
        super().__init__(all_emails)
        self._q_functions: list = []

    def apply_filter(self, filter : BasicExchangeFilter):
        self._q_functions.append(filter.get_query_function())
        return self

    def get_emails(self):
        if len(self._q_functions) == 0:
            return self._all_available_emails.all()

        q = self._q_functions[0]
        for i in range(1, len(self._q_functions)):
            q = q & self._q_functions[i]
        return self._all_available_emails.filter(q)


class ExchangeEmailProber(BasicEmailProber):

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

    def get_all_emails(self):
        return ExchangeEmailHolder(self._account.inbox)
