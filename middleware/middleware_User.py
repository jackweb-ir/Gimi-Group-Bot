from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from typing import Callable , Dict , Any , Awaitable
from db.db_user import dbUser
from aiogram.enums.chat_type import ChatType



class CheckUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        
        if(event.chat.type == ChatType.PRIVATE):
            
            idUser = event.from_user.id

            check_user = await dbUser.check(idUser)
            
            if(check_user != True):
                
                await dbUser.insert(idUser)
      
        return await handler(event, data)