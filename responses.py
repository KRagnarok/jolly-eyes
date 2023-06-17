
from datetime import datetime
from typing import Dict, List, Union
from pydantic import BaseModel

from protocols.basic.filters import *
from protocols.basic.visitor import BasicFilterVisitor


class EmailResponse(BaseModel):
    id: int
    email_address: str
    protocol: str

class BaseFilter(BaseModel):
    options: Optional[Dict[str, str]]

    def fill_filter(self, visitor: BasicFilterVisitor) -> BasicEmailFilter:
        raise NotImplementedError()

class SubjectFilter(BaseFilter):
    subject: str

    def fill_filter(self, visitor: BasicFilterVisitor) -> BasicEmailFilter:
        subject_filter = visitor.get_subject_filter()
        return subject_filter(self.options, self.subject)

class AuthorFilter(BaseFilter):
    author: str

    def fill_filter(self, visitor: BasicFilterVisitor) -> BasicEmailFilter:
       author_filter = visitor.get_author_filter()
       return author_filter(self.options, self.author) 

class DateFilter(BaseFilter):
    start_date: datetime.datetime
    end_date: datetime.datetime

    def fill_filter(self, visitor: BasicFilterVisitor) -> BasicEmailFilter:
       date_filter = visitor.get_date_filter()
       return date_filter(self.options, start_date=self.start_date, end_date=self.end_date) 

class UnreadFilter(BaseFilter):
    
    def fill_filter(self, visitor: BasicFilterVisitor) -> BasicEmailFilter:
       unread_filter = visitor.get_unread_filter()
       return unread_filter(self.options) 

class Filter(BaseModel):
    filter_type: str
    filter_body: Union[
            SubjectFilter,
            AuthorFilter,
            DateFilter,
            UnreadFilter
    ]

class EmailFilterRequest(BaseModel):
    email_id: int
    filters: List[Filter]


class EmailInfo(BaseModel):
    email: str
    subject: str
    author: str
    # date: datetime.datetime

class EmailFilterResponse(BaseModel):
    emails: List[EmailInfo]


