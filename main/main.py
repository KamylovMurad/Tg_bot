import logging
from config import bot, db
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
import asyncio
from statesform import AdminStates
from handlers import start, sub_chan_done, admin_command, \
    get_text, confirm_send_admin, get_users_count
from aiogram.contrib.fsm_storage.memory import MemoryStorage


async def main():
    await db.create_pool()
    await db.create_user_table()

    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    dp.register_message_handler(start, Command(commands=['start']))
    dp.register_callback_query_handler(
        sub_chan_done,
        lambda c: c.data == 'sub_done'
    )
    dp.register_message_handler(admin_command, commands=['send'])
    dp.register_message_handler(get_text, state=AdminStates.distribute)
    dp.register_callback_query_handler(
        confirm_send_admin,
        lambda c: c.data in ['confirm', 'cancel'],
        state=AdminStates.distribute
    )
    dp.register_message_handler(get_users_count, commands=['count'])

    try:
        await dp.start_polling(bot)
    except Exception as ex:
        logging.error(f'[!!! Exception] - {ex}', exc_info=True)
    finally:
        await bot.session.close()

if __name__ == '__main__':
    asyncio.run(main())
