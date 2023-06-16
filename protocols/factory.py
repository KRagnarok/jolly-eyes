from .basic.connector import BasicEmailConnector, EmailAccountInfo
from .exchange.connector import ExchangeEmailConnector
from .imap.connector import IMAPEmailConnector

from .basic.filters import BasicEmailFilter
from .exchange.filters import *
from .imap.filters import *

available_protocols = {
            "Exchange": ExchangeEmailConnector,
            "IMAP": IMAPEmailConnector
}

class ProtocolFactory():

    @staticmethod
    def create(protocol: str, account_info: EmailAccountInfo) -> BasicEmailConnector:
        protocol_class = available_protocols.get(protocol, None)
        if protocol_class == None:
            raise Exception("The provided protocol does not exist")

        return protocol_class(account_info)

available_filters = {
        "Exchange": available_exchange_filters,
        "IMAP": available_imap_filters
}

class FilterFactory():

    @staticmethod
    def _get_filter_class(protocol: str, filter: str):
        protocol_filters = available_filters.get(protocol, None)
        if protocol_filters == None:
            raise Exception("The provided protocol does not exist")
        
        filter_class = protocol_filters.get(filter, None)
        if filter_class == None:
            raise Exception(f"The provided filter does not exist in the {protocol} implemented filters")

        return filter_class

    @staticmethod
    def filter_subject(protocol: str) -> BasicEmailSubjectFilter:
        return FilterFactory._get_filter_class(protocol, "subject")

    @staticmethod
    def filter_unread(protocol: str) -> BasicEmailUnreadFilter:
        return FilterFactory._get_filter_class(protocol, "unread")
                
    @staticmethod
    def filter_date(protocol: str) -> BasicEmailDateFilter:
        return FilterFactory._get_filter_class(protocol, "date")

    @staticmethod
    def filter_author(protocol: str) -> BasicEmailAuthorFilter:
        return FilterFactory._get_filter_class(protocol, "author")
     
       
