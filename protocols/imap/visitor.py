from typing import Type
from ..basic.visitor import BasicFilterVisitor

from .filters import *


class IMAPFilterVisitor(BasicFilterVisitor):

    def get_date_filter(self) -> Type[BasicEmailDateFilter]:
        return IMAPEmailDateFilter

    def get_author_filter(self) -> Type[BasicEmailAuthorFilter]:
        return IMAPEmailAuthorFilter

    def get_unread_filter(self) -> Type[BasicEmailUnreadFilter]:
        return IMAPEmailUnreadFilter

    def get_subject_filter(self) -> Type[BasicEmailSubjectFilter]:
        return IMAPEmailSubjectFilter
