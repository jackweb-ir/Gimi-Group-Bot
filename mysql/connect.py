import aiomysql
import config

class ConnectSql:
    
    def __init__(self):
        self.config = config.db_config

    async def run(self , sql : str , params=None):
        try:
            async with aiomysql.create_pool(**self.config) as pool:
                async with pool.acquire() as connect:
                    async with connect.cursor() as cursor:
                        await cursor.execute(sql, params)
                        await connect.commit()
            return True
        except:
            return False

    async def fethOne(self , sql : str , params=None):
        try:
            async with aiomysql.create_pool(**self.config) as pool:
                async with pool.acquire() as connect:
                    async with connect.cursor() as cursor:
                        await cursor.execute(sql, params)
                        result = await cursor.fetchone()
            return result
        except:
            return False

    async def fethAll(self , sql : str , params=None):
        try:
            async with aiomysql.create_pool(**self.config) as pool:
                async with pool.acquire() as connect:
                    async with connect.cursor() as cursor:
                        await cursor.execute(sql, params)
                        result = await cursor.fetchall()
            return result
        except:
            return False

ConnectSql = ConnectSql()
        
        
                    
