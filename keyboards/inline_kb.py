from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_callback_buttons(
      sizes: tuple[int] = (3,)  
):
    keyboard = InlineKeyboardBuilder()
    btn1 = InlineKeyboardButton(text='United States Dollar', callback_data='USD')
    btn2 = InlineKeyboardButton(text='Canadian Dollar', callback_data='CAD')
    btn3 = InlineKeyboardButton(text='Euro', callback_data='EUR')
    btn4 = InlineKeyboardButton(text='Japanese Yen', callback_data='JPY')
    btn5 = InlineKeyboardButton(text='Chinese Yuan', callback_data='CNY')
    btn6 = InlineKeyboardButton(text='British Pound', callback_data='GBP')
    btn7 = InlineKeyboardButton(text='Swiss Franc', callback_data='CHF')
    btn8 = InlineKeyboardButton(text='New Zealand Dollar', callback_data='NZD')
    btn9 = InlineKeyboardButton(text='Australian Dollar', callback_data='AUD')
    btn10 = InlineKeyboardButton(text='South Korean Won', callback_data='KRW')
    btn11 = InlineKeyboardButton(text='Polish Zloty', callback_data='PLN')
    btn12 = InlineKeyboardButton(text='Danish Krone', callback_data='DKK')
    btn13 = InlineKeyboardButton(text='Turkish New Lira', callback_data='TRY')
    btn14 = InlineKeyboardButton(text='Hong Kong Dollar', callback_data='HKD')

    keyboard.add(btn1, btn2, btn3, btn4, btn5, btn6, btn7, btn8, btn9, btn10, btn11, btn12, btn13, btn14)

    return keyboard.adjust(*sizes).as_markup()