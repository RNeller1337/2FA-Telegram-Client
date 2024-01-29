import json
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from utils.database import Database
from utils.auth import start

logging.basicConfig(level=logging.INFO)

with open('etc/config.json', 'r') as f:
    config = json.load(f)
bot = Bot(token=config['token'])

dp = Dispatcher()


@dp.message(Command("start"))
async def start_commands(message: types.Message):
    await message.answer(
        'Привет!\nЯ бот, позволяющий получать одноразовые коды для аунтификации в сервисах, требующих 2FA.\nИспользуйте /help для просмотра списка команд.')


@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(
        'Список команд:\n/add <название> <2FA ключ> - Добавить 2FA ключ в бота.\n/remove <название> - Удалить 2FA ключ из бота.\n/get <название> - Получить одноразовый код.\n/list - Показать список добавленных 2FA ключей.\n/help - Показать список команд.')


@dp.message(Command("add"))
async def add_command(message: types.Message):
    await db.create_table()
    args = message.text.split()[1:]
    if len(args) < 2:
        await message.answer('Недостаточно аргументов. Пример: /add <название> <2FA ключ>')
    else:
        user_id = message.from_user.id
        name = args[0]
        key = ' '.join(args[1:])
        check = await db.get_key(user_id, name)
        if check:
            await message.answer('Ключ с таким названием уже существует.')
        else:
            await db.add_key(user_id, name, key)
            await message.answer('Ключ успешно добавлен.')


@dp.message(Command("remove"))
async def remove_command(message: types.Message):
    await db.create_table()
    args = message.text.split()[1:]
    if len(args) < 1:
        await message.answer('Недостаточно аргументов. Пример: /remove <название>')
    else:
        user_id = message.from_user.id
        name = args[0]
        check = await db.get_key(user_id, name)
        if not check:
            await message.answer('Ключа с таким названием не существует.')
        else:
            await db.remove_key(user_id, name)
            await message.answer('Ключ успешно удален.')


@dp.message(Command("list"))
async def list_command(message: types.Message):
    await db.create_table()
    user_id = message.from_user.id
    keys = await db.get_all(user_id)
    if not keys:
        await message.answer('У вас нет добавленных 2FA ключей.')
    else:
        text = 'Список добавленных 2FA ключей:\n'
        for name, key in keys:
            text += f'{name}: {key}\n'
        await message.answer(text)


@dp.message(Command("get"))
async def get_command(message: types.Message):
    await db.create_table()
    args = message.text.split()[1:]
    if len(args) < 1:
        await message.answer('Недостаточно аргументов. Пример: /get <название>')
    else:
        user_id = message.from_user.id
        name = args[0]
        key = await db.get_key(user_id, name)
        if not key:
            await message.answer('Ключа с таким названием не существует.')
        else:
            try:
                token = start(key[0])
            except Exception:
                return await message.answer(f'Произошла ошибка. Убедитесь, что ваш 2FA ключ введён верно.')
            await message.answer(f'Ваш одноразовый код для {name}: {token}')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    db = Database()
    asyncio.run(main())
