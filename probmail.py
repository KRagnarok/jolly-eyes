#!/usr/bin/python3
from protocols.basic.connector import EmailAccountInfo
from protocols.exchange.filters import ExchangeEmailAuthorFilter
from protocols.factory import ProtocolFactory, FilterFactory


def main():
    # exh = IMAPEmailProber(email_acc_info=email_info)
    exh = ProtocolFactory.create("Exchange", email_info)
    exh.connect_and_auth()
    holder = exh.get_all_emails()
    # holder.apply_filter(IMAPEmailSubjectFilter(subject='instance'))

    subject_filter_cls = FilterFactory.filter_unread("Exchange") 
    # subject_filter_obj = subject_filter_cls(options= {
        # "contains": True,
        # "like": True}, subject="net")

    holder.apply_filter(subject_filter_cls(options=None))
    for item in holder.get_emails():
        print(item.subject)
    # for item in exh.get_new_emails():
        # print(item.subject)
    # print(exh.get_new_emails().count())


if __name__ == '__main__':
    main()
