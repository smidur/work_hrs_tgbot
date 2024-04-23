from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import texts


def get_keyboards(kbd: str):
    builder = InlineKeyboardBuilder()

    match kbd:
        case "start":
            builder.add(
                InlineKeyboardButton(text=texts.button_clock_in, callback_data="announce_in"),
                InlineKeyboardButton(text=texts.button_clock_out, callback_data="announce_out"),
                InlineKeyboardButton(text=texts.button_settings, callback_data="settings")
            )
            builder.adjust(2, 1)
        case "announce_general":
            builder.add(
                InlineKeyboardButton(text=texts.button_clock_in, callback_data="announce_in"),
                InlineKeyboardButton(text=texts.button_clock_out, callback_data="announce_out")
            )
        case "announce_in":
            builder.add(
                InlineKeyboardButton(text=texts.button_manual_entry, callback_data="manual_entry_in"),
                InlineKeyboardButton(text=texts.button_clock_in, callback_data="clock_in")
            )
        case "announce_out":
            builder.add(
                InlineKeyboardButton(text=texts.button_manual_entry, callback_data="manual_entry_out"),
                InlineKeyboardButton(text=texts.button_clock_out, callback_data="clock_out")
            )
        case "clock_in":
            builder.add(
                InlineKeyboardButton(text=texts.button_manual_entry, callback_data="manual_entry"),
                InlineKeyboardButton(text=texts.button_clock_out, callback_data="announce_out")
            )
        case "clock_out":
            builder.add(
                InlineKeyboardButton(text=texts.button_manual_entry, callback_data="manual_entry"),
                InlineKeyboardButton(text=texts.button_clock_in, callback_data="announce_in")
            )
        case "edit":
            print("EDIT not implemented yet")
        case "settings":
            print("SETTINGS not implemented yet")

    return builder.as_markup()


