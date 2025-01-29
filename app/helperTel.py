
async def sendMessageReply (bot , message , text:str):
    await bot.send_message(
        chat_id=message.chat.id,
        text= text,
        reply_to_message_id=message.message_id,
        parse_mode="html"
    )
    
async def sendMessageButtom (bot , message , text:str , keyboard):
    await bot.send_message(
        chat_id=message.chat.id,
        text= text,
        reply_markup=keyboard,
        parse_mode="html"
    )
    
async def sendphoto (bot , message , photo , text:str):
    await bot.send_photo(
        chat_id= message.chat.id,
        photo= photo,
        caption= text,
        reply_to_message_id= message.message_id,
        parse_mode="html"
    )