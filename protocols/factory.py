from .basic.connector import EmailAccountInfo
from .exchange.connector import ExchangeEmailConnector
from .imap.connector import IMAPEmailConnector

available_protocols = {
            "Exchange": ExchangeEmailConnector,
            "IMAP": IMAPEmailConnector
}

class ProtocolFactory():

    @staticmethod
    def create(protocol: str, account_info: EmailAccountInfo):
        protocol_class = available_protocols.get(protocol, None)
        if protocol_class == None:
            raise Exception("The provided protocol does not exist")

        return protocol_class(account_info)
        
