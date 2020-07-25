from aiogram.types import Message
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import types

from main import bot, dp
from config import admin_id
from keyboards import main_menu, menu_brends
from states.special_shoes import SpecialShoes
import sqlite3

async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text="Бот запущен")
    

@dp.message_handler(commands=['start'])
async def send_welcome(message: Message):
    await message.answer(
        '<strong>Привет!</strong> Погнали за скидками!\nВыберете пункт ниже:', 
        reply_markup=main_menu
    )

@dp.message_handler(Text("Обувь с мультибрендовых сайтов"))
async def multi_shoes(message: Message):
    parse_sh() 
    conn = sqlite3.connect('lamoda_shoes.db')
    c = conn.cursor()

    SQL_STRING = 'SELECT * FROM sales ORDER BY random() LIMIT 10'
    c.execute(SQL_STRING)

    items = c.fetchall()

    for item in items:
        title = item[1]
        link = item[2]
        price = item[3]
        await message.answer(f"<strong>Модель:</strong> {title}\n\n<strong>Ссылка:</strong> <em>{link}</em>\n\n<strong>Цена:</strong> {price} UAH") 

@dp.message_handler(Text("Одежда с мультибрендовых сайтов"))
async def multi_clothes(message: Message):
    parse_cl()    
    conn = sqlite3.connect('lamoda_clothes.db')
    c = conn.cursor()

    SQL_STRING = 'SELECT * FROM sales ORDER BY random() LIMIT 10'
    c.execute(SQL_STRING)

    items = c.fetchall()
    
    for item in items:
        title = item[1]
        link = item[2]
        price = item[3]
        await message.answer(f"<strong>Модель:</strong> {title}\n\n<strong>Ссылка:</strong> <em>{link}</em>\n\n<strong>Цена:</strong> {price} UAH") 


@dp.message_handler(Text("Подобрать обувь"), state=None)
async def enter_test(message: types.Message):
    await message.answer("Время подобрать обувь специально для вас!\n"
                         "Здесь вы можете выбрать размер, цену и бренд,а бот подберет пару со скидкой "
                         "<strong>для вас!</strong>\n\n "
                         "Мужские или женские?\n (Для ответа писать капсом МУЖ/ЖЕН)")

    await SpecialShoes.Q1.set()

@dp.message_handler(state=SpecialShoes.Q1)
async def answer_q1(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer1=answer)

    await message.answer("Введите самую большу цену, которую вы готовы заплатить (в UAH):")

    await SpecialShoes.next()

@dp.message_handler(state=SpecialShoes.Q2)
async def answer_q2(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(answer2=answer)

    await message.answer("Введите бренд, который вас интересует:", reply_markup=menu_brends)

    await SpecialShoes.next()

@dp.message_handler(state=SpecialShoes.Q3)
async def answer_q3(message: types.Message, state: FSMContext):
    
    answer = message.text
    await state.update_data(answer3=answer)
    # Достаем переменные
    data = await state.get_data()
    answer1 = data.get("answer1")
    answer2 = data.get("answer2")
    answer3 = data.get("answer3")

    await message.answer(
        "Минутку, бот уже ищет для обувь именно для вас. Процес может занять до 2-3 минут.\n"
        "Обувь будет посортирована по возростанию цены."   )
    conn = sqlite3.connect('../lamoda/lamoda/lamoda_shoes.db')
    c = conn.cursor()

    SQL_STRING = "SELECT * FROM sales WHERE sex = '"+answer1.lower()+"' AND price < " + answer2 +" AND brand LIKE '%"+ answer3.lower() +"%' ORDER BY price"
    print(SQL_STRING)
    c.execute(SQL_STRING)
    
    items = c.fetchall()
    if len(items) != 0:
        for item in items:
            brand = item[1]
            title = item[2]
            link = item[3]
            price = item[4]
            photo = item[5]
            sizes = item[6]
            await message.answer(f"<strong>Модель:</strong> {title}, {brand}\n\n<strong>Ссылка:</strong> <em>{link}</em>\n\n<strong>Цена:</strong> {price} UAH\n\n<strong>Рарзмера в наличии:</strong> {sizes}\n\n<strong>Фото:</strong> {photo}", reply_markup=main_menu)
    else:
        await message.answer(
            "По вашему запросу ничего не найдено.\n\n"
            "Проверьте данные, которые вы ввели: \n"
            "Ответ на первый вопрос должен быть только <strong>МУЖ</strong> или <strong>ЖЕН</strong>\n"
            "Ответ на второй вопрос должен быть числом, без пробелов, без указания валюты, например: <strong>1200</strong>\n"
            "Ответ на третий вопрос <strong>должен быть выбран с меню.</strong>\n\n"
            "Если вы уверены, что всё ввели коррекно, вполне может быть, что в разделе скидок нет обуви, которая соответсвует вашим критериям.",
            reply_markup=main_menu
            )
    
    await state.finish()
