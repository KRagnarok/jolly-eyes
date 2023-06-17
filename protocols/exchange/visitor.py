from typing import Type
from ..basic.visitor import BasicFilterVisitor

from .filters import *

class ExchangeFilterVisitor(BasicFilterVisitor):

    def get_date_filter(self) -> Type[BasicEmailDateFilter]:
        return ExchangeEmailDateFilter

    def get_author_filter(self) -> Type[BasicEmailAuthorFilter]:
        return ExchangeEmailAuthorFilter

    def get_unread_filter(self) -> Type[BasicEmailUnreadFilter]:
        return ExchangeEmailUnreadFilter

    def get_subject_filter(self) -> Type[BasicEmailSubjectFilter]:
        return ExchangeEmailSubjectFilter


