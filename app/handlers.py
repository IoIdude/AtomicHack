import requests
from aiogram.filters import Command
from main import client
from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.enums.chat_action import ChatAction
from aiogram.types import Message, Chat, FSInputFile
from fsm.states import WaitState
from modules.photo_alg import download_photo
from sources.messages import MESSAGES
from utils.config import API

router = Router()


@router.message(WaitState.msgPrinted)
async def wait_print_answ(message: Message):
    await message.answer(MESSAGES['wait_print_answ'])


@router.message(Command('start'))
async def start(message: Message):
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)

    pin = await message.answer(MESSAGES['pin_msg'])
    chat: Chat = await client.get_chat(message.chat.id)

    if chat.pinned_message:
        if (chat.pinned_message.text.replace(' ', '').replace('\n', '') == MESSAGES['pin_msg']
                .replace(' ', '').replace('\n', '')):
            await client.unpin_chat_message(chat_id=message.chat.id)

    await client.pin_chat_message(chat_id=message.chat.id, message_id=pin.message_id)
    await message.answer(MESSAGES['pin_info'])


@router.message(Command('history'))
async def history(message: Message):
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)

    pin = await message.answer(MESSAGES['pin_msg'])
    chat: Chat = await client.get_chat(message.chat.id)

    if chat.pinned_message:
        if (chat.pinned_message.text.replace(' ', '').replace('\n', '') == MESSAGES['pin_msg']
                .replace(' ', '').replace('\n', '')):
            await client.unpin_chat_message(chat_id=message.chat.id)

    await client.pin_chat_message(chat_id=message.chat.id, message_id=pin.message_id)
    await message.answer(MESSAGES['pin_info'])


@router.message(F.photo)
async def send_photo(message: Message, state: FSMContext):
    await state.set_state(WaitState.msgPrinted)
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)

    path = await download_photo(message)
    files = {'file': open(path, "rb")}
    headers = {'Accept': 'application/json'}
    response = requests.post(API, files=files, headers=headers)
    files['file'].close()

    if response.status_code == 200:
        response_json = response.json()

        image_url = response_json['output']['image']
        classes = response_json['output']['results']

        string_results = '· #' + '\n· #'.join(classes)
        img_response = requests.get(image_url)

        if img_response.status_code == 200:
            path = await download_photo(image_url, img_response)
            await message.answer_photo(
                FSInputFile(path=path), caption=string_results
            )
        else:
            await message.reply(MESSAGES['error'])
    else:
        await message.reply(MESSAGES['error'])

    await state.clear()


@router.message(F.text)
async def idk_text(message: Message):
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    await message.answer(MESSAGES['idk_text'])
