from aiogram import types, Router, F, Bot
from dataclass import datagroup
from aiogram.filters import ChatMemberUpdatedFilter, MEMBER, IS_NOT_MEMBER, Command
from handlers.client import CallbackFactory

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

class FSMAdmin(StatesGroup):
    answer = State()


router = Router()
router.my_chat_member.filter(F.chat.type.in_({"group", "supergroup"}))
router.message.filter(F.chat.type.in_({"group", "supergroup"}))
router.callback_query.filter(F.message.chat.type.in_({"group", "supergroup"}))


async def event_add_in_group(event: types.ChatMemberUpdated, bot: Bot):
    datagroup.id_group = event.chat.id

    await bot.send_message(
        chat_id=event.chat.id,
        text=f"Вас приветствует бот Bazar Family, в группе администраторов, я буду присылать сюда отзывы клиентов, на которые вы сможете ответить"
    )


async def callback_answer(event: types.CallbackQuery, callback_data: CallbackFactory, state: FSMContext):
    await state.set_state(FSMAdmin.answer)
    await state.update_data(chat_id=callback_data.client_chat_id)

    await event.message.answer(f"Админ {event.from_user.username} напишите ответ или отмените коммандой /cancel!")


async def admin_answer(message: types.Message, state: FSMContext, bot: Bot):
    print("eeee")
    await message.reply("Спасибо за ответ)")

    data = await state.update_data()

    await bot.send_message(data['chat_id'], message.text)

    await state.clear()


async def command_cancel(message: types.Message, state: FSMContext):
    await message.answer(f"Отмена действия для администратора - {message.from_user.username}")
    await state.clear()


async def command_id(message: types.Message):
    await message.answer(f"id вашего чата: {message.chat.id}")


def register_admingroup():
    router.message.register(command_id, Command(commands="id"))
    router.message.register(command_cancel, Command(commands="cancel"), state=FSMAdmin.answer)
    router.message.register(admin_answer, state=FSMAdmin.answer)
    router.my_chat_member.register(event_add_in_group, ChatMemberUpdatedFilter(member_status_changed=IS_NOT_MEMBER >> MEMBER))
    router.callback_query.register(callback_answer, CallbackFactory.filter())

    return router
