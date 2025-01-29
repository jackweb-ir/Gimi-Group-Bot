import app.installLibraries as installLibrarie
from config import bot_config , list_libraries

installLibrarie.install(list_libraries)

import asyncio
import jdatetime
import html

from aiogram import F , Bot , Dispatcher
from aiogram.enums.chat_type import ChatType
from aiogram.types import Message
from aiogram.types.reply_keyboard_markup import ReplyKeyboardMarkup
from aiogram.types.reply_keyboard_remove import ReplyKeyboardRemove
from aiogram.types.keyboard_button import KeyboardButton

from middleware.middleware_User import CheckUserMiddleware

import app.helperTel as Tel
from app.digitalCurrency import Currency

from db.db_group import dbGroup
from db.db_user import dbUser


TOKEN = bot_config['token']
ADMIN = bot_config['admin']

bot = Bot(token = TOKEN)
dp = Dispatcher()
nowTime = jdatetime.datetime.now()


dp.message.middleware(CheckUserMiddleware())

@dp.message((F.text.regexp(r'^[\/][Ss][Tt][Aa][Rr][Tt]$') & F.chat.type == ChatType.PRIVATE))
async def messages(message: Message):
    await Tel.sendMessageReply(bot , message , "<b>Welcome to the robot.</b>")


#------------------------- PRIVATE ADMIN ----------------------------


@dp.message((F.text.regexp(r'^(/panel|panel|پنل)$') & F.chat.type == ChatType.PRIVATE) & (F.from_user.id.in_(ADMIN)))
async def messages(message: Message):
    buttom1 = KeyboardButton(text="آمار ربات")
    buttom2 = KeyboardButton(text="لیست گروه ها")
    buttom3 = KeyboardButton(text="دستورات ادمین")
    buttom4 = KeyboardButton(text="بستن")
    keyboard = ReplyKeyboardMarkup(keyboard= [[buttom1 , buttom2],[buttom3],[buttom4]],  resize_keyboard=True)
    return await Tel.sendMessageButtom(bot , message , "<b>به پنل مدیریت خوش آمدید</b>" ,keyboard)


@dp.message((F.text.regexp(r'^(بستن)$') & F.chat.type == ChatType.PRIVATE) & (F.from_user.id.in_(ADMIN)))
async def messages(message: Message):
    
    keyboard = ReplyKeyboardRemove(remove_keyboard=True)
    return await Tel.sendMessageButtom(bot , message , "<b>با موفقیت پنل بسته شد</b>" ,keyboard)


@dp.message((F.text.regexp(r'^(آمار ربات)$') & F.chat.type == ChatType.PRIVATE) & (F.from_user.id.in_(ADMIN)))
async def messages(message: Message):
    
    countGroup = await dbGroup.fethCount()
    countUser = await dbUser.fethCount()
    time = nowTime.strftime(r"%H:%M:%S")
    date = nowTime.strftime(r"%a, %d %b %Y")

    return await Tel.sendMessageReply(bot , message , f"📊 آمار ربات در {date} | {time} به شرح زیر است:\n\n👤 آمار کاربران : {countUser}\n👥 آمار گروه ها نصب شده : {countGroup}\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬")


@dp.message((F.text.regexp(r'^(لیست گروه ها)$') & F.chat.type == ChatType.PRIVATE) & (F.from_user.id.in_(ADMIN)))
async def messages(message: Message):
    
    resultGroup = await dbGroup.fethAll()
    
    if resultGroup == ():
        return await Tel.sendMessageReply(bot , message , "<b>لیست خالی میباشد 🔴</b>")

    resulttext = "<b>🟢 لیست 20 گروه آخر به شرح زیر است :\n\n"
    
    for index , group in enumerate(resultGroup):
        if index > 20:
            break
        idGroup = group[0]
        try:
            pyloadInfo = await bot.get_chat(chat_id=idGroup)
            titleGap = html.escape(pyloadInfo.title)
        except Exception as e:
            titleGap = "نامشخص"
        resulttext += f"Group{index+1} : <code>{idGroup}</code> | {titleGap} \n" 
    
    resulttext += r"▬▬▬▬▬▬▬▬▬▬▬▬▬▬</b>"

    return await Tel.sendMessageReply(bot , message , resulttext)


@dp.message((F.text.regexp(r'^(دستورات ادمین)$') & F.chat.type == ChatType.PRIVATE) & (F.from_user.id.in_(ADMIN)))
async def messages(message: Message):
    
    return await Tel.sendMessageReply(bot , message , "🟢 دستورات ادمین داخل گروه :\n\n\n❗️نصب ربات در گروه :\n◆ دستور 1 : ( نصب ربات یا install )◄ فقط در گروه کار میکند.\n◆ دستور 2 : ( نصب ربات یا install **** )◄ همه جا کار میکند و به جای ستاره، ایدی عددی گروه را بزارید.\n══════════════════\n❗️ حذف نصب :\n◆ دستور 1 : ( حذف نصب یا uninstall )◄ فقط در گروه کار میکند.\n◆ دستور 2 : (  حذف نصب یا uninstall  **** )◄ همه جا کار میکند و به جای ستاره، ایدی عددی گروه را بزارید.\n══════════════════\n❗️ گرفتن ایدی عددی گروه :\n◆ دستور : ( ایدی گروه یا id gap ) ◄ فقط در گروه کار میکند.\n\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬")


#------------------------- TYPE ALL ADMIN ----------------------------


@dp.message((F.text.regexp(r'^(uninstall|حذف نصب) -[0-9]+$')) & (F.from_user.id.in_(ADMIN)))
async def messages(message: Message):
    chatId = message.text.replace('uninstall ', '') 
    chatId = int(chatId.replace('حذف نصب ', ''))

    
    if chatId > 0:
        return await Tel.sendMessageReply(bot , message , "<b>➖ آیدی عددی وارد شده اشتباه است.</b>")
    
    if await dbGroup.remove(chatId) != True:
        return await Tel.sendMessageReply(bot , message , "<b>➖ در فرایند حذف مشکل ایجاد شد</b>")
        
    return await Tel.sendMessageReply(bot , message , "<b>✅ با موفقیت حذف شد</b>")


@dp.message((F.text.regexp(r'^(install|نصب ربات) -[0-9]+$')) & (F.from_user.id.in_(ADMIN)))
async def messages(message: Message):
    chatId = message.text.replace('install ', '') 
    chatId = int(chatId.replace('نصب ربات ', ''))

    
    if chatId > 0:
        return await Tel.sendMessageReply(bot , message , "<b>➖ آیدی عددی وارد شده اشتباه است.</b>")
    
    if await dbGroup.check(chatId) != True :
        if await dbGroup.insert(chatId) != True:
            return await Tel.sendMessageReply(bot , message , "<b>➖ در فرایند نصب مشکل ایجاد شد</b>")
            
        return await Tel.sendMessageReply(bot , message , "<b>✅ با موفقیت نصب شد</b>")
            
    return await Tel.sendMessageReply(bot , message , "<b>➖ این گروه قبلا نصب شده است</b>")


@dp.message( (F.text.regexp(r'^(id gap|ایدی گروه)$')) & (F.from_user.id.in_(ADMIN)) )
async def messages(message: Message):
    
    chatId = message.chat.id
    chatTitle = html.escape(message.chat.title)
    resultText = f'✦ نام گروه: {chatTitle}\n✦ شناسه گروه: <code>{chatId}</code>\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬'
    
    return await Tel.sendMessageReply(bot , message , resultText)


#------------------------- GROUP ADMIN ----------------------------


@dp.message(F.text.regexp(r'^(install|نصب ربات)$') & ((F.chat.type == ChatType.SUPERGROUP) | (F.chat.type == ChatType.GROUP)) & (F.from_user.id.in_(ADMIN)))
async def messages(message: Message):
    chatId = message.chat.id
    
    if message.chat.type == ChatType.GROUP:
        return await Tel.sendMessageReply(bot , message , "<b>❌ ربات فقط در سوپر گروه ها قابل نصب است</b>")
        
    if await dbGroup.check(chatId) != True :
        if await dbGroup.insert(chatId) != True:
            return await Tel.sendMessageReply(bot , message , "<b>➖ در فرایند نصب مشکل ایجاد شد</b>")
            
        return await Tel.sendMessageReply(bot , message , "<b>✅ با موفقیت نصب شد</b>")
            
    return await Tel.sendMessageReply(bot , message , "<b>➖ این گروه قبلا نصب شده است</b>")


@dp.message((F.text.regexp(r'^(uninstall|حذف نصب)$') & F.chat.type == ChatType.SUPERGROUP) & (F.from_user.id.in_(ADMIN)))
async def messages(message: Message):
    chatId = message.chat.id
    if await dbGroup.remove(chatId) != True:
        return await Tel.sendMessageReply(bot , message , "<b>➖ در فرایند حذف مشکل ایجاد شد</b>")
        
    return await Tel.sendMessageReply(bot , message , "<b>✅ با موفقیت حذف شد</b>")


#------------------------- GROUP ALL ----------------------------


@dp.message((F.text.regexp(r'^(help|راهنما)$') & F.chat.type == ChatType.SUPERGROUP))
async def messages(message: Message):
    chatId = message.chat.id
    if await dbGroup.check(chatId) != True :
        return
            
    return await Tel.sendMessageReply(bot , message , "🟢 راهنمای ربات :\n\n\n❗️ گرفتن قیمت کل ارز ها :\n◆ دستور : ( نرخ ارز   یا   قیمت ارز )\n══════════════════\n❗️ گرفتن قیمت ارز خاص :\n◆ دستور : ( قیمت **** ) ◄ به جای ستاره اسم ارز مورد نظر را بنویسید.\n══════════════════\n❗️ گرفتن مشخصات خود یا کاربر مورد نظر :\n◆ دستور : ( ایدی یا id ) ◄ اگر مشخصات کاربر مورد نظر را میخواهید این دستور را روی آن ریپلی کنید.\n\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬")


@dp.message((F.text.regexp(r'^(نرخ ارز|قیمت ارز)$') & F.chat.type == ChatType.SUPERGROUP))
async def messages(message: Message):
    chatId = message.chat.id
    if await dbGroup.check(chatId) != True :
        return
    
    Fa = await Currency.getCurrencyToStrFa()
    En = await Currency.getCurrencyToStrEn()
    time = nowTime.strftime(r"%H:%M:%S")
    date = nowTime.strftime(r"%a, %d %b %Y")
            
    return await Tel.sendMessageReply(bot , message , f"╣[ نرخ ارز :\n\n• تاریخ :  {date}\n• ساعت : {time}\n\n{Fa}\n\n══════════════════\n\n{En}")


@dp.message((F.text.regexp(r'^(قیمت) .+$') & F.chat.type == ChatType.SUPERGROUP))
async def messages(message: Message):
    chatId = message.chat.id
    if await dbGroup.check(chatId) != True :
        return
    
    text = message.text.replace('قیمت ', '')
    
    Fa = await Currency.getCurrencyToStrSinglFa(text)
    En = await Currency.getCurrencyToStrSinglEn(text)
    
    if Fa == False or En == False:
        return
    
    time = nowTime.strftime(r"%H:%M:%S")
    date = nowTime.strftime(r"%a, %d %b %Y")
            
    return await Tel.sendMessageReply(bot , message , f"▨ قیمت ارز 「{text}」 :\n\n• تاریخ :  {date}\n• ساعت : {time}\n\n{Fa}\n{En}\n══════════════════")
            
            
@dp.message((F.text.regexp(r'^(id|ایدی|آیدی)$') & F.chat.type == ChatType.SUPERGROUP))
async def messages(message: Message):
    chatId = message.chat.id
    if await dbGroup.check(chatId) != True :
        return

    fromID = message.reply_to_message.from_user.id if message.reply_to_message else message.from_user.id
    nameUser = message.reply_to_message.from_user.first_name if message.reply_to_message else message.from_user.first_name
    tagName = f'<a href="tg://user?id={fromID}">{html.escape(nameUser)}</a>'
    UserProfilePhotos = await bot.get_user_profile_photos(fromID,1,1)
    fileIdPhoto = UserProfilePhotos.photos[0][-1].file_id if UserProfilePhotos.photos else False
    resultText = f'✦ نام: {tagName}\n✦ شناسه: <code>{fromID}</code>\n✦ شناسه گروه: <code>{chatId}</code>\n\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬'
    
    if fileIdPhoto:
        return await Tel.sendphoto(bot,message , fileIdPhoto , resultText)
    else:
        return await Tel.sendMessageReply(bot , message , resultText)
    
    
#------------------------- Bot Run ----------------------------


async def main():
    await dp.start_polling(bot , polling_timeout = 30)
    
print('🟢🟢🟢🟢🟢🟢 bot run')

asyncio.run(main())