import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
import requests

from keyboards.inline_kb import get_callback_buttons
from keyboards.reply_kb import get_convert_kb, get_menu_kb, get_start_kb


load_dotenv()

api_key = os.getenv("API_KEY")

token = os.getenv("TOKEN")

bot = Bot(token)

dp = Dispatcher()


class UserConvertInfo(StatesGroup):
    count = State()
    amount = State()
    from_ = State()
    to_ = State()
    convert = State()


@dp.message(CommandStart())
async def start(message: types.Message, state: FSMContext):
    await state.set_state(UserConvertInfo.count)
    await state.update_data(count=0)
    await message.answer_dice()
    await message.answer(f'Hi, <b>{message.from_user.first_name}</b>!\n Enter amount to convert. \n It should be a number.', parse_mode=ParseMode.HTML, reply_markup=get_menu_kb())

    await state.set_state(UserConvertInfo.amount)
    

@dp.message(F.text == '/convert')
async def convert_currency(message: types.Message, state: FSMContext):
    data = await state.get_data()

    try:
        api_url = f'https://api.api-ninjas.com/v1/convertcurrency?want={data["to_"]}&have={data["from_"]}&amount={data["amount"]}'
        response = requests.get(api_url, headers={'X-Api-Key': api_key})
            
        await message.answer(
            f'<b>{data["amount"]} {data["from_"]} = {response.json()["new_amount"]} {data["to_"]}</b>', parse_mode=ParseMode.HTML,
            reply_markup=get_start_kb()
            )
        await state.clear()
    except KeyError:
        await message.answer('Not enough data')
    

@dp.message(F.text.lower() == 'currency symbols')
async def currency_symbols(message: types.Message):
    await message.answer('USD - United States Dollar\n'  
                         'EUR - Euro\n'                  
                         'JPY - Japanese Yen\n'
                         'CNY - Chinese Yuan\n'          
                         'GBP - British Pound\n'
                         'CHF - Swiss Franc\n'           
                         'NZD - New Zealand Dollar\n'
                         'AUD - Australian Dollar\n'     
                         'KRW - South Korean Won\n'
                         'PLN - Polish Zloty\n'         
                         'DKK - Danish Krone\n'
                         'TRY - Turkish New Lira\n'
                         'HKD - Hong Kong Dollar \n'
                         'CAD - Canadian Dollar \n'
                         )



@dp.message(UserConvertInfo.amount)
async def get_amount(message: types.Message, state: FSMContext):
    try:
        amount = float(message.text)
        if amount <= 0:
            await message.answer('You must enter a positive number. Please, try again')
        else:
            await state.update_data(amount=amount)
            data = await state.get_data()
            await message.answer(
                f'Amount to convert: <b>{data["amount"]}</b>',
                parse_mode=ParseMode.HTML
                )
            await state.set_state(UserConvertInfo.from_)
            await convert_from(message)
    except ValueError:
         await message.answer('You must enter a positive number. Please, try again')
         return
    

async def convert_from(message: types.Message):
    await message.answer('Select currency to convert', reply_markup=get_callback_buttons())
    
        
@dp.message(UserConvertInfo.to_)
async def convert_to(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await message.answer(f'Select currency you want to convert <b>{data["amount"]} {data["from_"]}</b> into', reply_markup=get_callback_buttons(), parse_mode=ParseMode.HTML)
    
    

@dp.callback_query(UserConvertInfo.from_)
async def callback_data(callback: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if data["count"] == 0:
        await state.update_data(from_=callback.data)
        await callback.message.edit_reply_markup()
        await callback.message.delete()
        data = await state.get_data()
        await callback.message.answer(f'Converting <b>{data["amount"]} {data["from_"]}</b>', parse_mode=ParseMode.HTML)
        await state.update_data(count=1)
        await convert_to(callback.message, state) 
    else:
        await state.update_data(to_=callback.data)
        data = await state.get_data()
        await callback.message.edit_reply_markup()
        await callback.message.delete()
        await state.update_data(count=0)
        data = await state.get_data()
        await callback.message.answer(f'Converting <b>{data["amount"]} {data["from_"]} into {data["to_"]}</b>\n   Press "/convert" button', reply_markup=get_convert_kb(), parse_mode=ParseMode.HTML)
        await state.set_state(UserConvertInfo.convert)


@dp.message(UserConvertInfo.from_)
async def bot_answers(message: types.Message):
    await message.answer('Select currency using keyboard') 


@dp.message(UserConvertInfo.convert)
async def bot_answers(message: types.Message):
    await message.answer('Press <b>CONVERT</b> button', parse_mode=ParseMode.HTML) 
        

async def main():
    await dp.start_polling(bot)


asyncio.run(main())




