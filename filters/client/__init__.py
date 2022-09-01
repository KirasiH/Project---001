from aiogram.filters import BaseFilter
from aiogram import types
from aiogram.fsm.context import FSMContext


class ClientAudioOrMessageFilter(BaseFilter):

    async def __call__(self, message: types.Message, state: FSMContext):
        if message.content_type == "text":
            await state.update_data(feedback_text=message.text)
            await state.update_data(feedback_voice=None)
            return True

        elif message.content_type == "voice":
            await state.update_data(feedback_voice=message.voice.file_id)
            await state.update_data(feedback_text=None)
            return True

        await message.answer(f"Отправте либо аудио, либо текст, ваще сообщение типа {message.content_type}")
        return
