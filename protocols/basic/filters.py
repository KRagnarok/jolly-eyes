import datetime
from typing import Optional

class BasicEmailFilter():

    def __init__(self, options: Optional[dict]) -> None:
        self._options = options

    def get_filter_func(self):
        raise NotImplementedError()

class BasicEmailSubjectFilter(BasicEmailFilter):

    def __init__(self, options: Optional[dict], subject: str) -> None:
        super().__init__(options)
        self._subject = subject

    def get_filter_func(self):
        return super().get_filter_func()

class BasicEmailDateFilter(BasicEmailFilter):

    def __init__(self, options: Optional[dict], start_date: datetime.datetime,
                    end_date: datetime.datetime) -> None:
        super().__init__(options)
        self._start_date = start_date
        self._end_date = end_date

    def get_filter_func(self):
        return super().get_filter_func()

class BasicEmailAuthorFilter(BasicEmailFilter):

    def __init__(self, options: Optional[dict], author: str) -> None:
        super().__init__(options)
        self._author = author

    def get_filter_func(self):
        return super().get_filter_func()


class BasicEmailUnreadFilter(BasicEmailFilter):

    def __init__(self, options: Optional[dict]) -> None:
        super().__init__(options)

    def get_filter_func(self):
        return super().get_filter_func()


