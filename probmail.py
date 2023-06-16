#!/usr/bin/python3
from email_prober import *
from exchange_prober import *
from imap_prober import *


def main():
    # exh = IMAPEmailProber(email_acc_info=email_info)
    exh = ExchangeEmailProber(email_acc_info=email_info)
    exh.connect_and_auth()
    holder = exh.get_all_emails()
    # holder.apply_filter(IMAPEmailSubjectFilter(subject='instance'))
    for item in holder.get_emails():
        print(item.subject)
    # for item in exh.get_new_emails():
        # print(item.subject)
    # print(exh.get_new_emails().count())


if __name__ == '__main__':
    main()
