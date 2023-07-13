from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import CHANNEL_URL, url

sub_chan_button = InlineKeyboardButton(text='Подписаться', url=CHANNEL_URL)
sub_done = InlineKeyboardButton(text='Подписался', callback_data='sub_done')

CheckMenu = InlineKeyboardMarkup(row_width=1)
CheckMenu.add(sub_chan_button, sub_done)

download_button = InlineKeyboardButton(
  text='Скачать ТЗ',
  url=url,
  callback_data='link'
)
download = InlineKeyboardMarkup()
download.add(download_button)


admin_mark = InlineKeyboardMarkup(row_width=1)
cancel_button = InlineKeyboardButton(text='Омена', callback_data='cancel')
confirm_button = InlineKeyboardButton(
  text='Подтвердить',
  callback_data='confirm'
)
admin_mark.add(confirm_button, cancel_button)
