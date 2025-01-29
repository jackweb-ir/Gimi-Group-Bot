from mysql.connect import ConnectSql


class db_user:
    
    def __init__(self):
        self.connectDB = ConnectSql

    async def insert(self , id : int):
        sql = "INSERT INTO `users` (`id`) VALUES (%s) ;"
        return await self.connectDB.run(sql , (id))

    async def check(self , id : int):
        sql = "SELECT * FROM `users` WHERE `id` = '%s' LIMIT 1 ;"
        return bool(await self.connectDB.fethOne(sql , (id)))
        
    async def fethCount(self ):
        sql = "SELECT COUNT(`id`) FROM `users` ;"
        return (await self.connectDB.fethOne(sql))[0]
                    
dbUser = db_user()
