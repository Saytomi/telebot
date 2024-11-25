import asyncio
from aiogram import Bot, Dispatcher


from app.handlers import router


async def main():
    bot = Bot(token='8196844648:AAGbcXDftfvqknJjZ2KefWLM42fPdCAl4q8')
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)



if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print('Бот выключен')