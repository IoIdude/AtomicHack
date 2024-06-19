import os
import uuid
from multipledispatch import dispatch
from requests import Response
from aiogram.types import Message
from main import client


@dispatch(Message)
async def download_photo(message):
    photo = message.photo[-1]
    file_info = await client.get_file(photo.file_id)
    file_path = file_info.file_path
    file_data = await client.download_file(file_path)

    unique_id = uuid.uuid4().hex
    base_name = os.path.splitext(os.path.basename(file_path))[0]
    type_name = os.path.splitext(os.path.basename(file_path))[1]
    path = f'sources/user_data/{base_name}{unique_id}{type_name}'

    with open(path, "wb") as f:
        f.write(file_data.read())

    return path


@dispatch(str, Response)
async def download_photo(image_url, img_response):
    base_name = os.path.splitext(os.path.basename(image_url))[0]
    type_name = os.path.splitext(os.path.basename(image_url))[1]
    path = f'sources/res_imgs/{base_name}{type_name}'

    with open(path, "wb") as img_file:
        img_file.write(img_response.content)

    return path
