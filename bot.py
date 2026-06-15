import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

TOKEN = "8653856711:AAFtBnm45kIEWjACBWBwcJMUeraAM7i2RYs"

bot = Bot(token=TOKEN)
dp = Dispatcher()




main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="👉 О компании"),
            KeyboardButton(text="🖥 Сделать заказ")
        ],
        [
            KeyboardButton(text="📝 Оставить отзыв")
        ]
    ],
    resize_keyboard=True 
)



class FeedbackStates(StatesGroup):
    waiting_for_name = State()   
    waiting_for_text = State()   



@dp.message(F.text == "/start")
async def cmd_start(message: Message, state: FSMContext):
    await state.clear() 
    await message.answer(
        text="Ниже у вас открылось главное меню бота 👇",
        reply_markup=main_keyboard
    )


@dp.message(F.text == "🖥 Сделать заказ")
async def make_order(message: Message):
    
    catalog_inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Открыть каталог 📦", url="https://google.com")]
        ]
    )
    await message.answer(
        text="По кнопке ниже вы можете перейти в наш каталог и оформить заказ:",
        reply_markup=catalog_inline_kb
    )


@dp.message(F.text == "👉 О компании")
async def about_company(message: Message):
    text_about = (
        "«Как вы это привезли?» — это:\n\n"
        "Самые лучшие деликатесы с их исторической родины.\n\n"
        "Где самый лучший пармезан? В Италии!\n\n"
        "Где лучшие сыры?\nВ Европе!\n\n"
        "Где лучший хамон?\nВ Испании!\n\n"
        "Где лучшая икра?\nНа Дальнем Востоке!\n\n"
        "Как это все привезти?\nМы знаем!\n\n"
        "Мы привозим лучшие деликатесы из разных уголков мира и вы "
        "можете купить их с доставкой до вашего дома.\n\n"
        "За 2023 год - мы поучаствовали в 78 мероприятиях в Москве, "
        "Санкт-Петербурге, Краснодаре, Ставрополе, Тюмени, Екатеринбурге и других городах.\n\n"
        "Открыли магазин - кафе в самом центре СПб.\n\n"
        "Доставляем самые вкусные деликатесы со всего мира, прямо до вашей квартиры."
    )
    await message.answer(text=text_about)

@dp.message(F.text == "📝 Оставить отзыв")
async def start_feedback(message: Message, state: FSMContext):
    await message.answer("1. Напишите ваше имя")
    await state.set_state(FeedbackStates.waiting_for_name)


@dp.message(FeedbackStates.waiting_for_name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(user_name=message.text) # Сохраняем имя
    await message.answer("2. Напишите ваш отзыв")
    await state.set_state(FeedbackStates.waiting_for_text)


@dp.message(FeedbackStates.waiting_for_text)
async def process_feedback_text(message: Message, state: FSMContext):
    user_data = await state.get_data()
    user_name = user_data.get("user_name")
    feedback_text = message.text
    
    
    print(f"\n--- ПОЛУЧЕН НОВЫЙ ОТЗЫВ ---")
    print(f"Имя: {user_name}")
    print(f"Отзыв: {feedback_text}")
    print(f"---------------------------\n")

    await message.answer(
        text="Спасибо за ваш отзыв! Он уже ушел напрямую директору компании ❤️"
    )
    await message.answer(
        text="Главное меню",
        reply_markup=main_keyboard
    )
    await state.clear()

async def main():
    print("Бот успешно запущен и слушает команды...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
