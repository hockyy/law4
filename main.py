import os

import aiofiles as aiofiles
from dotenv import load_dotenv
from fastapi import FastAPI, File, UploadFile
from fastapi.openapi.utils import get_openapi
from starlette import status
from starlette.responses import JSONResponse

from model import Account, ErrorResponse

load_dotenv()

app = FastAPI()

try:
    os.makedirs("uploaded")
except:
    pass

def custom_openapi():
    """
    Sets up description for openAPI
    """
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Lab 4 - Hocky Yudhiono",
        version="1.0.0",
        description="CRUD",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi

database = dict()


def common_error(err: Exception):
    """
    Returns abnormal JSONResponse
    """
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        content=ErrorResponse("invalid request", f"{str(err)}").dict())


@app.get("/mahasiswa/{id}")
async def cek_mahasiswa(id: int):
    try:
        isi = database[id]
        if (isi): isi = isi.json
        return isi
    except Exception as e:
        return common_error(e)


@app.post("/mahasiswa")
async def daftar_mahasiswa(account: Account):
    try:
        database[account.id] = account
        return database[account.id].dict()
    except Exception as e:
        return common_error(e)


@app.put("/mahasiswa/{id}")
async def ganti_data(id: int, account: Account):
    account.id = id
    try:
        database[id] = account
        return database[id].dict()
    except Exception as e:
        return common_error(e)


@app.delete("/mahasiswa/{id}")
async def hapus_mahasiswa(id: int):
    try:
        del database[id]
        return {"message": "OK"}
    except Exception as e:
        return common_error(e)


@app.get("/")
async def print_all():
    semua = dict()
    for k, v in database.items():
        semua[k] = v.dict()
    return semua


@app.post("/files")
async def create_upload_file(file: UploadFile = File(...)):
    async with aiofiles.open(f"uploaded/{file.filename}", 'wb') as out_file:
        while content := await file.read(1024):  # async read chunk
            await out_file.write(content)  # async write chunk
    return {"filename": file.filename}
