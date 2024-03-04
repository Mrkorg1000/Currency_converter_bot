from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_menu_kb():
    menu_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="Currency symbols"),
            ]
        ], resize_keyboard=True,
    )
    return menu_kb

def get_convert_kb():
    convert_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="/convert"),
            ]
        ], one_time_keyboard=True, 
        resize_keyboard=True,
    )
    return convert_kb


def get_start_kb():
    start_kb = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="/start"),
            ]
        ], resize_keyboard=True,
    )
    return start_kb