import json
from typing import Any, Optional

from pydantic import BaseModel

class Account(BaseModel):
    def __init__(self, nama, alamat, id = 0, **data: Any):
        super().__init__(**data)
        self.nama = nama
        self.alamat = alamat
        self.id = id
    id : Optional[str] = None
    nama: Optional[str] = None
    alamat: Optional[str] = None


class ErrorResponse(BaseModel):
    def __init__(self, error: str, error_description: str, **data: Any):
        super().__init__(**data)
        self.error = error
        self.error_description = error_description

    error: str = "invalid_token"
    error_description: str = "Ada kesalahan masbro!"
