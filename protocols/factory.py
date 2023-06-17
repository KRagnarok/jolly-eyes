from .basic.connector import BasicEmailConnector, EmailAccountInfo
from .exchange.connector import ExchangeEmailConnector
from .imap.connector import IMAPEmailConnector

from .basic.visitor import BasicFilterVisitor
from .exchange.visitor import ExchangeFilterVisitor
from .imap.visitor import IMAPFilterVisitor

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

available_filter_visitors = {
        "Exchange": ExchangeFilterVisitor,
        "IMAP": IMAPFilterVisitor
}

class FilterVisitorFactory():

    @staticmethod
    def create_filter_visitor(protocol: str) -> BasicFilterVisitor:
        protocol_filter_visitor = available_filter_visitors.get(protocol, None)
        if protocol_filter_visitor == None:
            raise Exception("The provided protocol does not exist")

        return protocol_filter_visitor()
        
