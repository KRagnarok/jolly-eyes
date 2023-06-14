#!/usr/bin/python3
from email_prober import *
from exchange_prober import *


def main():
    exh = ExchangeEmailProber(email_acc_info=email_info)
    exh.connect_and_auth()
    # for item in exh.get_new_emails():
        # print(item.subject)
    print(exh.get_new_emails().count())


if __name__ == '__main__':
    main()
