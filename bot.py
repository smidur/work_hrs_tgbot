import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command

import texts
from keyboards import *
from config import env
from backend import *

# enable logging to see important messages
logging.basicConfig(level=logging.INFO)
# bot object
bot = Bot(token=env.TOKEN)
# dispatcher
dp = Dispatcher()
# databases
work_hrs_db = Database()
# settings_db = Settings()
# datetime set
date_time = DateTime()


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    # username = message.from_user.username
    # lastname = message.from_user.last_name
    # firstname = message.from_user.first_name
    # is_premium = message.from_user.is_premium

    work_hrs_db.create(user_id)

    await message.answer(text=texts.cmd_start_inmsg, reply_markup=get_keyboards("start"))


@dp.callback_query(F.data == "announce_in")
async def announce_in(call: types.CallbackQuery):
    dt = date_time.clock_in()
    dt_txt = date_time.datetime_to_str(dt)
    announce = texts.cmd_announce_in_inmsg % dt_txt
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text=announce, reply_markup=get_keyboards("announce_in"))


@dp.callback_query(F.data == "announce_out")
async def announce_out(call: types.CallbackQuery):
    dt = date_time.clock_out()
    dt_txt = date_time.datetime_to_str(dt)
    announce = texts.cmd_announce_out_inmsg % dt_txt
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text=announce, reply_markup=get_keyboards("announce_out"))


@dp.callback_query(F.data == "clock_in")
async def clock_in(call: types.CallbackQuery):
    dt_txt = date_time.clock_in_time
    user_id = call.from_user.id
    work_hrs_db.insert(user_id, "clock_in", dt_txt)
    clock_in_success = texts.success_clock_in % dt_txt
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text=clock_in_success)
    await bot.send_message(chat_id=call.from_user.id, reply_to_message_id=call.message.message_id,
                           text=texts.propose_clock_out,
                           reply_markup=get_keyboards("clock_in"))


@dp.callback_query(F.data == "clock_out")
async def clock_out(call: types.CallbackQuery):
    dt_txt = date_time.clock_out_time
    user_id = call.from_user.id
    work_hrs_db.insert(user_id, "clock_out", dt_txt)
    clock_out_success = texts.success_clock_out % dt_txt
    await bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                text=clock_out_success)
    await bot.send_message(chat_id=call.from_user.id,
                           text=texts.propose_clock_in,
                           reply_markup=get_keyboards("clock_out"))


# start polling process to wait for updates from telegram server
async def main():
    commands = [
        types.BotCommand(command=texts.cmd_start),
        types.BotCommand(command=texts.cmd_settings, description=texts.cmd_settings_descr),
        types.BotCommand(command=texts.cmd_help, description=texts.cmd_help_descr),
    ]
    await bot.set_my_commands(commands=commands, scope=types.BotCommandScopeDefault())
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
