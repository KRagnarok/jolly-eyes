from ..basic.connector import BasicEmailHolder, BasicEmailConnector, EmailAccountInfo
from ..basic.filters import BasicEmailFilter
from exchangelib import DELEGATE, Account, Configuration, Credentials

class ExchangeEmailHolder(BasicEmailHolder):

    def __init__(self, all_emails) -> None:
        super().__init__(all_emails)
        self._q_functions: list = []

    def apply_filter(self, filter : BasicEmailFilter):
        self._q_functions.append(filter.get_filter_func())
        return self

    def get_emails(self):
        if len(self._q_functions) == 0:
            return self._all_available_emails.all()

        q = self._q_functions[0]
        for i in range(1, len(self._q_functions)):
            q = q & self._q_functions[i]
        return self._all_available_emails.filter(q)


class ExchangeEmailConnector(BasicEmailConnector):

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

    def get_all_emails(self) -> BasicEmailHolder:
        return ExchangeEmailHolder(self._account.inbox)
