from dataclasses import dataclass
import json
from typing import List

from protocols.basic.connector import EmailAccountInfo

@dataclass
class Protocol():
    protocol_type: str

@dataclass
class Account():
    email_auth_info: EmailAccountInfo
    protocol: Protocol

class Config():

    def __init__(self, path_to_config: str) -> None:
        self._path_to_config = path_to_config
        
    def parse_config(self):
        with open(self._path_to_config, 'r') as f:
            self._config = json.load(f)

    def get_accounts(self) -> List[Account]:
        accounts_list = self._config["accounts"]
        accounts = []

        for acc in accounts_list:
            accounts.append(
                Account(
                    email_auth_info=EmailAccountInfo(
                        email_address=acc["email_address"],
                        username=acc["username"],
                        password=acc["password"],
                        server_address=acc["server_address"],
                        server_port=acc.get("server_port", -1),
                    ),
                    protocol=Protocol(
                        protocol_type=acc["protocol"]["protocol_type"]
                    )
                )
            )

        self._accounts = accounts
        return accounts
            
