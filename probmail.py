#!/usr/bin/python3
from email_prober import *
from exchange_prober import *


def main():
    exh = ExchangeEmailProber(email_options=email_info)
    exh.connect_and_auth()
    for item in exh.get_all_emails():
        print(item.subject)


if __name__ == '__main__':
    main()
