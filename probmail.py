#!/usr/bin/python3
from logging import warn
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from config import *
from protocols.factory import ProtocolFactory, FilterVisitorFactory 
from responses import *


app = FastAPI()

accounts: List[Account] = []

def auth_and_get_auth_obj(acc: Account): 
    auth = ProtocolFactory.create(protocol=acc.protocol.protocol_type, account_info=acc.email_auth_info)
    auth.connect_and_auth()
    return auth

@app.on_event("startup")
async def startup():
    global accounts
    config = Config("./config.json")
    config.parse_config()
    accounts = config.get_accounts()  

@app.get("/email/list")
async def get_list_of_emails():
    list_of_emails = []
    for index, acc in enumerate(accounts):
        list_of_emails.append(EmailResponse(id=index,
                                email_address=acc.email_auth_info.email_address,
                                protocol=acc.protocol.protocol_type))
    
    return list_of_emails

@app.post("/filter-email")
async def get_emails(req: EmailFilterRequest) -> Response:
    if req.email_id < 0 or req.email_id >= len(accounts):
        return JSONResponse(
                content={"error": "the provided email_id is not present"},
                status_code=status.HTTP_404_NOT_FOUND)

    acc = accounts[req.email_id]
    auth = auth_and_get_auth_obj(acc)
    emails = auth.get_all_emails()
    filter_visitor = FilterVisitorFactory.create_filter_visitor(acc.protocol.protocol_type) 
    
    for filter in req.filters:
        print(filter)
        emails.apply_filter(
            filter.filter_body.fill_filter(filter_visitor)
        )

    emails_ret: List[EmailInfo] = []
    print(emails.get_emails())
    for email in emails.get_emails():
        emails_ret.append(
                EmailInfo(
                    email=acc.email_auth_info.email_address,
                    subject=email.subject,
                    author=email.author
                    # date=email.date
                )
        )


    return JSONResponse(
            content=jsonable_encoder(EmailFilterResponse(emails=emails_ret)),
            status_code=status.HTTP_200_OK)
        
