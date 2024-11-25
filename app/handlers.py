import sqlite3
from aiogram import F, Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from pathlib import Path


router = Router()

DB_FILE = "data.db"


def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(""" CREATE TABLE IF NOT EXISTS photos (id INTEGER PRIMARY KEY AUTOINCREMENT, file_id TEXT NOT NULL) """)
    cursor.execute("""CREATE TABLE IF NOT EXISTS documents (id INTEGER PRIMARY KEY AUTOINCREMENT, file_id TEXT NOT NULL) """)
    conn.commit()
    conn.close()

init_db()


def save_photo_id(file_id: str) -> None:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO photos (file_id) VALUES (?)", (file_id,))
    conn.commit()
    conn.close()

def save_document_id(file_id: str) -> None:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO documents (file_id) VALUES (?)", (file_id,))
    conn.commit()
    conn.close()

def get_all_photo_ids() -> list:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT file_id FROM photos")
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result

def get_all_document_ids() -> list:
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT file_id FROM documents")
    result = [row[0] for row in cursor.fetchall()]
    conn.close()
    return result


@router.message(CommandStart())
async def command_start_handler(message: Message):
    """
    /start buyrug'ini qayta ishlash: Foydalanuvchiga salom yuboradi
    """
    await message.answer(
        "Assalomu alaykum! 👋\n\n"
        "Men rasmlar va fayllarni saqlaydigan botman. Menga rasm yoki fayl yuboring, "
        "men uni saqlab qo'yaman.\n\n"
        "Barcha saqlangan rasmlar va fayllarni ko'rish uchun /rasmlar yoki /fayllar buyrug'ini ishlating."
    )

@router.message(F.photo)
async def photo_handler(message: Message):

    # Eng yuqori sifatli rasmni olamiz
    photo_data = message.photo[-1]

    # file_id ni bazaga saqlaymiz
    save_photo_id(photo_data.file_id)
    
    await message.answer("Rasm muvaffaqiyatli saqlandi! ✅")

@router.message(F.document)
async def document_handler(message: Message):
    """
    Fayllarni bazaga saqlash: Yangi kelgan fayllarni file_id ni saqlaydi
    """
    # file_id ni bazaga saqlaymiz
    save_document_id(message.document.file_id)

    await message.answer("Fayl muvaffaqiyatli saqlandi! ✅")

@router.message(Command("rasmlar"))
async def show_photos_handler(message: Message):

    photo_ids = get_all_photo_ids()
    if not photo_ids:
        await message.answer("Hozircha saqlangan rasmlar yo'q 😢\n"
                             "Menga rasm yuboring, men uni saqlab qo'yaman!")
        return
    
    await message.answer(f"Jami {len(photo_ids)} ta rasm topildi:")
    for photo_id in photo_ids:
        try:
            await message.answer_photo(photo=photo_id)
        except Exception:
            continue

@router.message(Command("fayllar"))


async def show_documents_handler(message: Message):
    document_ids = get_all_document_ids()
    if not document_ids:
        await message.answer("Hozircha saqlangan fayllar yo'q 😢\n"
                             "Menga fayl yuboring, men uni saqlab qo'yaman!")
        return
    
    await message.answer(f"Jami {len(document_ids)} ta fayl topildi:")
    for document_id in document_ids:
        try:
            await message.answer_document(document=document_id)
        except Exception:
            continue