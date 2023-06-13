from typing import Optional
from email_prober import EmailProber, EmailOptions, EmailFilter
from exchangelib import DELEGATE, Account, Configuration, Credentials


class ExchangeEmailProber(EmailProber):

    def __init__(self, email_options : EmailOptions):
        self._email_options = email_options
        self._is_connected = False

    def connect_and_auth(self):
        self._credentials = Credentials(
                username = self._email_options.username,
                password = self._email_options.password
        )
        self._config = Configuration(
                server = self._email_options.server_address,
                credentials = self._credentials
        )
        self._account = Account(
                primary_smtp_address = self._email_options.email_address,
                config = self._config,
                autodiscover = False,
                access_type = DELEGATE
        )
        self._is_connected = True

    def get_all_emails(self, filter: Optional[EmailFilter] = None):
        return self._account.inbox.all()

    def get_new_emails(self):
        return super().get_new_emails()
 
