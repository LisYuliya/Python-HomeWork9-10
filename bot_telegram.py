import time
import logging
from aiogram import Bot, Dispatcher, executor, types
import random
import os

# 'UTF-8-sig'
logging.basicConfig(level=logging.INFO, filename="bot_log.csv", filemode="w",
                    format="%(asctime)s: %(levelname)s %(funcName)s-%(lineno)d %(message)s")


MSG = "{}, choose an action:"

bot = Bot("6171153932:AAG3aPRLySj-V1Mipzwss0Apdxe1lFw8XxE")
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    user_full_name = message.from_user.full_name
    user_bot = message.from_user.is_bot
    user_message = message.text
    logging.info(f'{user_id=} {user_bot=} {user_message=}')
    await message.reply(f"Hi, {user_full_name}!")
    time.sleep(0)
    btns = types.ReplyKeyboardMarkup(row_width=3)
    btn_calc = types.KeyboardButton('/calculator')
    btn_photo = types.KeyboardButton('/photo')
    btn_out = types.KeyboardButton('/quit')
    btn_happy = types.KeyboardButton('/happy')
    btn_sad = types.KeyboardButton('/sad')
    btn_normal = types.KeyboardButton('/normal')
    btns.add(btn_calc, btn_out, btn_photo, btn_happy, btn_sad, btn_normal)
    await bot.send_message(user_id, MSG.format(user_name), reply_markup=btns)

@dp.message_handler(commands=['happy'])
async def quit_handler(message: types.Message):
    photo = open('mood/' + 'smile.jpg', 'rb')
    song = open('mood/' + 'zdob-si-zdub-videli-noch.mp3', 'rb')
    await bot.send_message(message.from_user.id, 'Заболел хорошим настроением… Больничный брать не буду! Пускай люди заражаются…=)')
    await bot.send_photo(message.from_user.id, photo)
    await bot.send_audio(message.from_user.id, song,
                         reply_markup=types.ReplyKeyboardMarkup())

@dp.message_handler(commands=['sad'])
async def quit_handler(message: types.Message):
    photo = open('mood/' + 'sad.jpg', 'rb')
    song = open('mood/' + 'Океан_Ельзи_feat_Один_В_Каное_Місто_Весни.mp3', 'rb')
    await bot.send_message(message.from_user.id, 'Бывают моменты, когда безумно грустно и одиноко. и вроде бы есть кому позвонить, но понимаешь, что всем не до тебя')
    await bot.send_photo(message.from_user.id, photo)
    await bot.send_audio(message.from_user.id, song,
                         reply_markup=types.ReplyKeyboardMarkup())
                         
@dp.message_handler(commands=['normal'])
async def quit_handler(message: types.Message):
    photo = open('mood/' + 'normal.jpg', 'rb')
    song = open('mood/' + 'Animal ДжаZ - Три Полоски.mp3', 'rb')
    await bot.send_message(message.from_user.id, 'Если хотите добиться успеха, задайте себе четыре следующих вопроса: Почему? А почему бы и нет? Почему бы и не я? Почему бы и не прямо сейчас?')
    await bot.send_photo(message.from_user.id, photo)
    await bot.send_audio(message.from_user.id, song,
                         reply_markup=types.ReplyKeyboardMarkup())

@dp.message_handler(commands=['photo'])
async def quit_handler(message: types.Message):
    photo = open('test/' + random.choice(os.listdir('test')), 'rb')
    await bot.send_photo(message.from_user.id, photo,
                         reply_markup=types.ReplyKeyboardMarkup())



@dp.message_handler(commands=['quit'])
async def quit_handler(message: types.Message):
    await bot.send_message(message.from_user.id, 'Goodbye! See you...',
                           reply_markup=types.ReplyKeyboardRemove())




value = ""
old_value = ""
keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
keyboard.row(types.InlineKeyboardButton("C", callback_data="C"),
             types.InlineKeyboardButton("<=", callback_data="<="),
             types.InlineKeyboardButton("(", callback_data="("),
             types.InlineKeyboardButton("/", callback_data="/"))
keyboard.row(types.InlineKeyboardButton("7", callback_data="7"),
             types.InlineKeyboardButton("8", callback_data="8"),
             types.InlineKeyboardButton("9", callback_data="9"),
             types.InlineKeyboardButton("*", callback_data="*"))
keyboard.row(types.InlineKeyboardButton("4", callback_data="4"),
             types.InlineKeyboardButton("5", callback_data="5"),
             types.InlineKeyboardButton("6", callback_data="6"),
             types.InlineKeyboardButton("-", callback_data="-"))
keyboard.row(types.InlineKeyboardButton("1", callback_data="1"),
             types.InlineKeyboardButton("2", callback_data="2"),
             types.InlineKeyboardButton("3", callback_data="3"),
             types.InlineKeyboardButton("+", callback_data="+"))
keyboard.row(types.InlineKeyboardButton("0", callback_data="0"),
             types.InlineKeyboardButton(",", callback_data="."),
             types.InlineKeyboardButton(")", callback_data=")"),
             types.InlineKeyboardButton("=", callback_data="="))


@dp.message_handler(commands=['calculator'])
async def start_handler(message: types.Message):
    await bot.send_message(message.from_user.id, "I open the calculator")
    if value == "":
        await bot.send_message(message.from_user.id, "0", reply_markup=keyboard)
    else:
        await bot.send_message(message.from_user.id, value, reply_markup=keyboard)


@dp.callback_query_handler(lambda c: True)
async def callback_calc(query):

    global value, old_value
    data = query.data

    if data == "C":
        value = ""
    elif data == "<=":
        if value != "":
            if len(value) == 1:
                value = ""
            else:
                value = value[:len(value)-1]
    elif data == "=":
        try:
            value = str(eval(value))
        except:
            value = "Error"
    else:
        value += data

    if (value != old_value and value != "") or ("0" != old_value and value == ""):
        if value == "":
            await bot.edit_message_text(chat_id=query.message.chat.id,
                                        message_id=query.message.message_id,
                                        text="0", reply_markup=keyboard)
            old_value = "0"
        else:
            await bot.edit_message_text(chat_id=query.message.chat.id,
                                        message_id=query.message.message_id,
                                        text=value, reply_markup=keyboard)

            old_value = value

    if value == "Error":
        value = ""

if __name__ == '__main__':
    executor.start_polling(dp)















