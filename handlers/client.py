from aiogram import types, Router, F, Bot
from aiogram.utils.keyboard import InlineKeyboardBuilder

from filters import ClientAudioOrMessageFilter
from aiogram.filters.callback_data import CallbackData
from aiogram.filters import Command

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from dataclass import datagroup


class CallbackFactory(CallbackData, prefix="fabnum"):
    client_chat_id: int


class FSMClient(StatesGroup):
    feedback = State()


router = Router()
router.my_chat_member.filter(F.chat.type.in_({"private"}))
router.message.filter(F.chat.type.in_({"private"}))
router.callback_query.filter(F.message.chat.type.in_({"private"}))


async def command_start(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(
        types.InlineKeyboardButton(text="на пл. Ленина", callback_data="на пл. Ленина"),
        types.InlineKeyboardButton(text="на Уинстонском пляже", callback_data="на Уинстонском пляже"),
        types.InlineKeyboardButton(text="на Шендриково", callback_data="на Шендриково"),
        types.InlineKeyboardButton(text="у театра \"Шут\"", callback_data="у театра \"Шут\"")
    )

    builder.adjust(1)

    await message.answer(
        "Добрый день! На связи Bazar Family Этот Бот создан для сбора обратной связи. В каком из наших заведений Вы находитесь или были",
        reply_markup=builder.as_markup()
    )


async def callback_massage(callback: types.CallbackQuery, state: FSMContext):

    await state.set_state(FSMClient.feedback)
    await state.update_data(institution=callback.data)

    await callback.message.edit_text(f"Расскажите о ваших впечатлениях о заведении - \"{callback.data}\". Мы принимаем обратную связь в виде текстового или голосового сообщения.Если у Вас возникли: вопрос, пожелания, претензия - можете написать в Бот. Оперативно Вам ответим. Спасибо❤️")

async def feedback(message: types.Message, state: FSMContext, bot: Bot):
    data = await state.update_data()
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Ответить", callback_data=CallbackFactory(client_chat_id=message.chat.id)
    )

    if not data['feedback_voice']:
        await bot.send_message(
            chat_id=datagroup.id_group,
            text=f"username: {message.from_user.id}\n"
                 f"Заведение: {data['institution']}, отзыв:\n"
                 f"{data['feedback_text']}",
            reply_markup=builder.as_markup()
        )

    else:
        await bot.send_voice(
            chat_id=datagroup.id_group,
            voice=data['feedback_voice'],
            caption=f"username: {message.from_user.id}\n"
                    f"Заведение: {data['institution']}",
            reply_markup=builder.as_markup()
        )

    await message.answer("Спасибо за обратную связь, скоро мы вернёмся с ответом!")
    await state.clear()


async def echo(message: types.Message):
    pass


def register_client():
    router.message.register(command_start, Command(commands=["start"]))
    router.callback_query.register(callback_massage)
    router.message.register(feedback, ClientAudioOrMessageFilter(), state=FSMClient.feedback)
    router.message.register(echo)

    return router
