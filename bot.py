import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import (
    Message,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove,
)
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

# ===================== SOZLAMALAR =====================
BOT_TOKEN = "8591331769:AAHAr-uBMoww2-1AaDCXma81crJWm65kIM8"
ADMIN_CHAT_ID = [ 7958070473, 639197405]  # <-- admin chat id sini yoz (int)

# ===================== MATN (https o‘rniga @) =====================
REKLAMA_TEXT = (
    "⚡️🤩TELEGRAM_YULDUZLARI @TYUZBEK КАНАЛИНИ РЕКЛАМА НАРХИ\n\n"
    "🛠 Маҳсулот ва хизматлар рекламаси:\n"
    "💰0/24 - 1 млн 500 минг сўм (топ йўқ.) Нархлар ўзгармайди\n\n"
    "@Toza_Toshkentliklar\n\n"
    "🛠 Маҳсулот ва хизматлар рекламаси:\n"
    "💰0/24 - 250 минг сўм\n\n"
    "@BORGAPUZ\n\n"
    "🛠 Маҳсулот ва хизматлар рекламаси:\n"
    "💰0/24 - 400 минг сўм\n\n"
    "🤖 Канал, гуруҳ ва ботлар рекламаси: ОЛИНМАЙДИ ❌\n\n"
    "Нархлар ўзгармайди ( бўлиши)\n\n"
    "❌ Реклама топ қўйилмайди! БИЗДА РЕКЛАМЛАР СОАТ 19:00ГАЧА ҚЎЙИЛАДИ.\n\n"
    "Бошқа каналларга ўхшаб бир кунда 48 та реклама жойламаймиз.\n\n"
    "Нархлар ва шартлар билан танишиб чиқib, @tyuzbekadmin ga yozing!"
)

# ===================== KLAVIATURALAR =====================
main_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📢 Reklama berish")],
        [KeyboardButton(text="☎️ Aloqa")],
    ],
    resize_keyboard=True,
)

back_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="⬅️ Ortga qaytish")]],
    resize_keyboard=True,
)

# ===================== STATE =====================
class ContactStates(StatesGroup):
    reklama = State()
    aloqa = State()

router = Router()

# ===================== /start =====================
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Assalomu alaykum! Kerakli bo‘limni tanlang:", reply_markup=main_kb)

# ===================== REKLAMA =====================
@router.message(F.text == "📢 Reklama berish")
async def reklama_menu(message: Message, state: FSMContext):
    await state.set_state(ContactStates.reklama)

    # eski keyboardni olib tashlaymiz
    await message.answer("Reklama bo‘limi:", reply_markup=ReplyKeyboardRemove())

    # reklama matni + ortga (preview o‘chiq emas)
    await message.answer(REKLAMA_TEXT, reply_markup=back_kb)

# ===================== ALOQA =====================
@router.message(F.text == "☎️ Aloqa")
async def aloqa_menu(message: Message, state: FSMContext):
    await state.set_state(ContactStates.aloqa)

    await message.answer("Aloqa bo‘limi:", reply_markup=ReplyKeyboardRemove())
    await message.answer("Habaringizni yozib qoldiring:", reply_markup=back_kb)

# ===================== ORTGA =====================
@router.message(F.text == "⬅️ Ortga qaytish")
async def go_back(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Bosh menyu:", reply_markup=main_kb)

# ===================== REKLAMA STATE: FORWARD =====================
@router.message(ContactStates.reklama)
async def reklama_forward(message: Message, bot: Bot):
    user = message.from_user

    # user yuborgan narsani (text/rasm/video/fayl) to‘liq forward
    await bot.forward_message(
        chat_id=ADMIN_CHAT_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
    )

    # qo‘shimcha info
    await bot.send_message(
        ADMIN_CHAT_ID,
        f"📢 Reklama bo‘limidan xabar\n"
        f"👤 {user.full_name} (@{user.username or 'username yo‘q'})\n"
        f"🆔 {user.id}"
    )

    await message.answer("✅ Habaringiz adminga yuborildi.")

# ===================== ALOQA STATE: FORWARD =====================
@router.message(ContactStates.aloqa)
async def aloqa_forward(message: Message, bot: Bot):
    user = message.from_user

    await bot.forward_message(
        chat_id=ADMIN_CHAT_ID,
        from_chat_id=message.chat.id,
        message_id=message.message_id,
    )

    await bot.send_message(
        ADMIN_CHAT_ID,
        f"☎️ Aloqa bo‘limidan xabar\n"
        f"👤 {user.full_name} (@{user.username or 'username yo‘q'})\n"
        f"🆔 {user.id}"
    )

    await message.answer("✅ Habaringiz adminga jo‘natildi.")

# ===================== RUN =====================
async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())