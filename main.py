
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
import asyncio
from crud_function import get_all_products

api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


kb_start = ReplyKeyboardMarkup(
    keyboard=
    [
        [KeyboardButton('Расчитать')],
        [KeyboardButton('Информация')],
        [KeyboardButton('Купить')]
    ],
    resize_keyboard=True
)

kb_inl = InlineKeyboardMarkup()
button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')


kb_inl.add(button1)
kb_inl.add(button2)

kb_inl_2 = InlineKeyboardMarkup()
button1_1 = InlineKeyboardButton(text='О нас', callback_data='about_us')
button2_1 = InlineKeyboardButton(text='Обратная связь', callback_data='contakt_us')

kb_inl_2.add(button1_1)
kb_inl_2.add(button2_1)

buy_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Product1", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product2", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product3", callback_data="product_buying")],
        [InlineKeyboardButton(text="Product4", callback_data="product_buying")]
    ]
)
#buy_kb = InlineKeyboardMarkup()
#butt1 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
#butt2 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
#butt3 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
#butt4 = InlineKeyboardButton(text="Product1", callback_data="product_buying")
#buy_kb.add(butt1, butt2, butt3, butt4)
@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer(f'Добро пожаловать {message.from_user.username} Я бот помогающий твоему здоровью', reply_markup=kb_start)


@dp.message_handler(text=['Расчитать'])
async def main_menu(message):
    await message.answer('Выберите опцию:',reply_markup=kb_inl)


@dp.message_handler(text=['Информация'])
async def inform(message):
    await message.answer('Здесь вы можете узнать всю информацию о нашем боте', reply_markup=kb_inl_2)



@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст:')
    await UserState.age.set()


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    try:
        await state.update_data(age=int(message.text))
    except:
        await message.answer('Введите число пожалуйста!')
    else:
        await message.answer("Ведите свой рост:")
        await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    try:
        await state.update_data(growth=int(message.text))
    except:
        await message.answer('Введите число пожалуйста!')
    else:
        await message.answer('Введите свой вес:')
        await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def set_calories(message, state):
    try:
        await state.update_data(weight=int(message.text))
    except:
        await message.answer('Введите число пожалуйста!')
    else:
        data = await state.get_data()
        await message.answer(f'Ваша суточная норма - {10 * data["weight"] + 6.25 * data["growth"] - 5 * data["age"] + 5} ккал')


    await state.finish()


@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('https://www.calc.ru/Formula-Mifflinasan-Zheora.html')


@dp.message_handler(text="Купить")
async def get_buying_list(message):
    for product in get_all_products():
        prod = dict(product)
        await message.answer(f"Название: {prod['title']} | Описание: {prod['description']} | Цена: {prod['price']}")
        with open(f"files/product{prod['id']}.png", "rb") as img:
            await message.answer_photo(img, parse_mode='HTML')

    await message.answer("Выберите продукт для покупки:", reply_markup=buy_kb)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)