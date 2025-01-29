from mysql.connect import ConnectSql



class db_group:
    
    def __init__(self):
        self.connectDB = ConnectSql

    async def insert(self , id : int):
        sql = "INSERT INTO `supergroups` (`group_id`) VALUES (%s);"
        return await self.connectDB.run(sql , (id))

    async def check(self , id : int):
        sql = "SELECT * FROM `supergroups` WHERE `group_id` = '%s' LIMIT 1 ;"
        return bool(await self.connectDB.fethOne(sql , (id)))
    
    async def fethOne(self , id : int):
        sql = "SELECT * FROM `supergroups` WHERE `group_id` = '%s' LIMIT 1 ;"
        return await self.connectDB.fethOne(sql , (id))
    
    async def remove(self , id : int):
        sql = "DELETE FROM `supergroups` WHERE `group_id` = '%s' ;"
        return await self.connectDB.run(sql , (id))
    
    async def fethAll(self ):
        sql = "SELECT `group_id` FROM `supergroups` ORDER BY `created_at` DESC;"
        return await self.connectDB.fethAll(sql)
    
    async def fethCount(self ):
        sql = "SELECT COUNT(`group_id`) FROM `supergroups` ;"
        return (await self.connectDB.fethOne(sql))[0]
        
                    
dbGroup = db_group()