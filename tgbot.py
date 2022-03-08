from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher #Считывание событий
from aiogram.utils import executor
from cfg import token
from time import sleep

#Crypto part(stats taken from ---> coinmarketcap.com)
from parseCrypto import Check_lofcoin, get_arr_stat

#To work with database
from wdb import Input_data, Check_on_exist, Change_loc, Check_loc, Check_lid, Change_lid

#Library to get messages after command
import aiogram.utils.markdown as md
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode

#Bot instruct and DB name
bot = Bot(token=token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
client_db = "users.db"
async def on_startup(_):
    print('Бот вышел в онлайн')
class Formv(StatesGroup):
    loc = State()

@dp.message_handler(commands=['start'])
async def commands_start(message : types.Message):
    try:
        await message.delete()
        if Check_on_exist(client_db, message.from_user.id) == 0:
            await bot.send_message(message.from_user.id, f"&#12840 Добро пожаловать, @{message.from_user.username} &#12840\nЯ &#129302 для парсинга курса криптовалют\nДля начала, укажите монеты, которые хотите спарсить &#128073 /loc", parse_mode='html')
            Input_data(client_db, message.from_user.id)
        else:
            await bot.send_message(message.from_user.id, f"С возвращением, @{message.from_user.username}\nДля обновления статистике, обновите сообщение выше\nИли же воспользуйтесь командой /encrypt", parse_mode='html')
    except Exception as e:
        print(repr(e))

@dp.message_handler(commands=['help', 'hlp', 'hp', 'поддержка'])
async def commands_start(message : types.Message):
    try:
        if Check_on_exist(client_db, message.from_user.id) == 0:
            Input_data(client_db, message.from_user.id)
        await message.reply(f"&#128206 Подробно о каждой из комманд &#128206\n\n├/start {md.hitalic('- приветственное сообщение')}\n├/enc {md.hitalic('- приветственное сообщение')}\n├/loc {md.hitalic('- внести новый список монет')}\n├/myl {md.hitalic('- проверить список своих монет')}", parse_mode='html')
    except: pass

@dp.message_handler(commands=['myl'])
async def commands_start(message : types.Message):
    try:
        if Check_on_exist(client_db, message.from_user.id) == 0:
            Input_data(client_db, message.from_user.id)
        await message.delete()
        f = await bot.send_message(message.from_user.id, "Подождите секунду... Ищу ваш список... &#9203", parse_mode='html')
        sleep(1.5)
        await f.delete()
        ans = Check_loc(client_db, message.from_user.id)
        if ans in [-1, 'none']:
            await bot.send_message(message.from_user.id, f"К сожалению, по вашему запросу нет записей &#128549\nНапишите команду /loc для написания нужного списка &#128203", parse_mode='html')
        else:
            await bot.send_message(message.from_user.id, f"Фух, кажется нашел &#128517\n\n{md.hitalic(f'{ans}')}", parse_mode='html')
    except: pass

@dp.message_handler(commands=['encrypt', 'enc', 'crypt'])
async def commands_start(message : types.Message):
    try:
        if Check_on_exist(client_db, message.from_user.id) == 0:
            Input_data(client_db, message.from_user.id)
        await message.delete()
        arr = Check_loc(client_db, message.from_user.id)
        if arr == 'none':
            await bot.send_message(message.from_user.id, "Не могу начать парсинг, ваш список крипто активов пуст\nПополните его с помощью команды /loc &#128521", parse_mode='html')
        elif arr not in [-1, 'none']:
            if Check_lid(client_db, message.from_user.id) == -1:
                await bot.send_message(message.from_user.id, "Непредвиденная ошибка")
            elif Check_lid(client_db, message.from_user.id) == 'none':
                f = await bot.send_message(message.from_user.id, "Начинаю парсинг... &#128187\n")
                await f.delete()
                ans = get_arr_stat(arr.split(', '))
                mess = await bot.send_message(message.from_user.id, f"{ans}", parse_mode='html')
                Change_lid(client_db, message.from_user.id, mess.message_id)
            else:
                idm = int(Check_lid(client_db, message.from_user.id))
                await bot.delete_message(message.from_user.id, message_id=idm)
                f = await bot.send_message(message.from_user.id, "Начинаю парсинг... &#128187\n")
                await f.delete()
                ans = get_arr_stat(arr.split(', '))
                mess = await bot.send_message(message.from_user.id, f"{ans}", parse_mode='html')
                Change_lid(client_db, message.from_user.id, mess.message_id)
    except Exception as e: print(repr(e))

@dp.message_handler(commands=['loc'])
async def cmd_start(message: types.Message):
    try:
        if Check_on_exist(client_db, message.from_user.id) == 0:
            Input_data(client_db, message.from_user.id)
        await Formv.loc.set()
        await message.reply("Введите через ',' все нужные монеты(не кратко)\nДля отмены, напишите команду 👉 /отмена")
    except: pass


# Добавляем возможность отмены, если пользователь передумал заполнять
@dp.message_handler(state='*', commands='cancel')
@dp.message_handler(Text(equals='отмена', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.finish()
    await message.reply("ввод остановлен")

@dp.message_handler(state=Formv.loc)
async def process_name(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['name'] = message.text
        loc = data['name'].split(', ')
        if Check_lofcoin(loc) != -1:
            Change_loc(client_db, message.from_user.id, data['name'])
            await bot.send_message(
                    message.from_user.id,
                    md.text(
                        md.text('✔ Новый лист монет записан ✔\nМожете проверить с помощью команды /myl'),
                        sep='\n',
                    )
                , parse_mode='html'
            )
            await state.finish()
        else:
            await bot.send_message(message.from_user.id, "Неккоректный ввод&#128269", parse_mode='html')
            await state.finish()
    except:
        try:
            await bot.send_message(message.from_user.id, "Неккоректный ввод&#128269", parse_mode='html')
            await state.finish()
        except: pass
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)