from aiogram import Bot, Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from crud_functions import initiate_db, get_all_products, add_products, add_user, is_included

API_TOKEN = ""
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Главная клавиатура с кнопками
main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add(KeyboardButton("Купить"), KeyboardButton("Информация"), KeyboardButton("Рассчитать"), KeyboardButton("Регистрация"))

# Inline меню для расчёта
calc_menu = InlineKeyboardMarkup(row_width=2)
calc_menu.add(
    InlineKeyboardButton("Рассчитать норму калорий", callback_data="calories"),
    InlineKeyboardButton("Формулы расчёта", callback_data="formulas")
)


# Состояния для регистрации
class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer("Добро пожаловать! Выберите действие из меню:", reply_markup=main_menu)


@dp.message_handler(text="Регистрация")
async def sing_up(message: types.Message):
    """Начало регистрации пользователя."""
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()


@dp.message_handler(state=RegistrationState.username)
async def set_username(message: types.Message, state: FSMContext):
    """Устанавливает имя пользователя."""
    username = message.text
    if is_included(username):
        await message.answer("Пользователь существует, введите другое имя:")
        return
    await state.update_data(username=username)
    await RegistrationState.email.set()
    await message.answer("Введите свой email:")


@dp.message_handler(state=RegistrationState.email)
async def set_email(message: types.Message, state: FSMContext):
    """Устанавливает email пользователя."""
    email = message.text
    await state.update_data(email=email)
    await RegistrationState.age.set()
    await message.answer("Введите свой возраст:")


@dp.message_handler(state=RegistrationState.age)
async def set_age(message: types.Message, state: FSMContext):
    """Устанавливает возраст пользователя и завершает регистрацию."""
    try:
        age = int(message.text)
        if age <= 0:
            raise ValueError
        await state.update_data(age=age)

        data = await state.get_data()
        add_user(data['username'], data['email'], data['age'])
        await state.finish()
        await message.answer("Вы успешно зарегистрированы!", reply_markup=main_menu)
    except ValueError:
        await message.answer("Возраст должен быть положительным числом. Попробуйте ещё раз:")


@dp.message_handler(text="Купить")
async def get_buying_list(message: types.Message):
    """Отправляет список продуктов из базы данных."""
    products = get_all_products()
    if not products:
        await message.answer("Нет доступных продуктов для покупки.")
        return

    buying_menu = InlineKeyboardMarkup(row_width=2)
    for product in products:
        product_id, title, description, price = product
        await message.answer_photo(
            photo=f"https://via.placeholder.com/150?text={title}",
            caption=f"Название: {title} | Описание: {description} | Цена: {price} руб."
        )
        buying_menu.add(InlineKeyboardButton(f"Купить {title}", callback_data=f"buy_{product_id}"))

    await message.answer("Выберите продукт для покупки:", reply_markup=buying_menu)


if __name__ == "__main__":
    # Инициализация базы данных
    initiate_db()
    add_products()

    # Запуск бота
    executor.start_polling(dp, skip_updates=True)
