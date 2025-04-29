
from datetime import datetime
import uuid

class Request:
    def __init__(self, client_id) -> None:
        self.client_id = client_id
        self.timestamp = int(datetime.now().timestamp() * 1000)
        self.request_id = str(uuid.uuid4())
    
    def __str__(self) -> str:
        return f"Request with Client ID {self.client_id} and timestamp is {self.timestamp}"