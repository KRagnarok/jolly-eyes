#!/usr/bin/python3
from config import *
from protocols.basic.connector import EmailAccountInfo
from protocols.exchange.filters import ExchangeEmailAuthorFilter
from protocols.factory import ProtocolFactory, FilterFactory

def main():
    config = Config("./config.json")
    config.parse_config()
    # print(config.get_accounts())

    acc1 = config.get_accounts()[0]
    auth = ProtocolFactory.create(protocol=acc1.protocol.protocol_type, account_info=acc1.email_auth_info)
    auth.connect_and_auth()
    emails = auth.get_all_emails()

    unread_filter = FilterFactory.filter_unread(protocol=acc1.protocol.protocol_type)
    emails.apply_filter(unread_filter(options=None))

    for em in emails.get_emails():
        print(em.subject)


if __name__ == '__main__': 
    main()
