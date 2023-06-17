from typing import Type
from .filters import *



class BasicFilterVisitor():

    def get_subject_filter(self) -> Type[BasicEmailSubjectFilter]:
        raise NotImplementedError()

    def get_author_filter(self) -> Type[BasicEmailAuthorFilter]:
        raise NotImplementedError()

    def get_date_filter(self) -> Type[BasicEmailDateFilter]:
        raise NotImplementedError()
    
    def get_unread_filter(self) -> Type[BasicEmailUnreadFilter]:
        raise NotImplementedError()
