import asyncio
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import RetryAfter, MessageNotModified
from config import bot, CHANNEL_ID, text, success_text, \
    unsuccess, admin_list, user_info
from statesform import AdminStates
from markups import CheckMenu, download, admin_mark
from config import db


async def bot_send_message(user_id, text, reply_markup=None):
    try:
        await bot.send_message(
            user_id, text,
            reply_markup=reply_markup,
            parse_mode='HTML'
        )
    except RetryAfter as e:
        await asyncio.sleep(e.timeout)
        return await bot_send_message(user_id, text, reply_markup)
    except Exception:
        return 1


async def check_sub_channel(chat_member):
    if chat_member['status'] != 'left':
        return True
    else:
        return False


async def get_url(username, user_id):
    if username is not None:
        return f'https://t.me/{username}'
    else:
        return f'<a href="tg://user?id={user_id}"' \
               f'>Ссылка на чат с пользователем</a>'


async def start(message: Message):
    if message.chat.type == 'private':
        username = message.from_user.username
        user_id = message.from_user.id
        url = await get_url(username, user_id)
        with open('Group 339.png', 'rb') as photo:
            try:
                await bot.send_photo(user_id, photo, caption=text)
            except RetryAfter as e:
                await asyncio.sleep(e.timeout)
                await bot.send_photo(user_id, photo, caption=text)
        for admin in admin_list:
            await bot_send_message(
                admin,
                user_info.format(
                    user_id,
                    'начал общение с ботом',
                    username,
                    url
                )
            )
        if await check_sub_channel(
                await bot.get_chat_member(
                    chat_id=CHANNEL_ID,
                    user_id=user_id
                )
        ):
            await bot_send_message(
                user_id,
                success_text,
                reply_markup=download
            )
            for admin in admin_list:
                await bot_send_message(
                    admin,
                    user_info.format(
                        user_id,
                        'подписался на канал',
                        username,
                        url
                    )
                )
            await db.set_user_id(user_id)
        else:
            await bot_send_message(
                user_id,
                'Подпишись на канал и возвращайся',
                reply_markup=CheckMenu
            )


async def sub_chan_done(call: CallbackQuery):
    user_id = call.from_user.id
    username = call.from_user.username
    url = await get_url(username, user_id)
    await bot.delete_message(user_id, call.message.message_id)
    await bot_send_message(user_id, 'Спасибо. Сейчас проверю')
    if await check_sub_channel(
            await bot.get_chat_member(
                chat_id=CHANNEL_ID,
                user_id=user_id
            )
    ):
        await bot_send_message(user_id, success_text, reply_markup=download)
        for admin in admin_list:
            await bot_send_message(
                admin,
                user_info.format(
                    user_id,
                    'подписался на канал',
                    username,
                    url
                    )
                )
        await db.set_user_id(user_id)
    else:
        await bot_send_message(user_id, unsuccess, reply_markup=CheckMenu)


async def admin_command(message: Message):
    user_id = message.from_user.id
    if user_id in admin_list:
        await bot_send_message(user_id, 'Введите текст для рассылки')
        await AdminStates.distribute.set()


async def get_text(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(text=message.text)
    await bot_send_message(
        user_id,
        'Выберите действие',
        reply_markup=admin_mark
    )


async def confirm_send_admin(call: CallbackQuery, state: FSMContext):
    try:
        await bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=None
        )
    except MessageNotModified:
        pass
    text = await state.get_data('text')
    await state.finish()
    user_id = call.from_user.id
    data = call.data
    count = 0
    if data == 'confirm':
        users_list = await db.get_users_list_to_distribute_for_all()
        if users_list:
            try:
                for user in users_list:
                    if not await bot_send_message(user, text.get("text")):
                        count += 1
                    await asyncio.sleep(0.1)
            finally:
                await bot_send_message(user_id,
                                       f'Рассылка закончена\n'
                                       f'Количество пользователей '
                                       f'получивших рассылку: {count}\n'
                                       )
        else:
            await bot_send_message(
                user_id,
                'Пользователи для рассылки не найдены'
            )


async def get_users_count(message: Message):
    user_id = message.from_user.id
    if user_id in admin_list:
        count = await db.cout_all()
        await bot_send_message(
            user_id,
            f'Кол-во подписанных пользователей: {count}'
        )
