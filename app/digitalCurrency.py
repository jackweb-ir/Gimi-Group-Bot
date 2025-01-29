import httpx
import json

class Currency():
    
    def __init__(self):
        self.urlCurrency = "https://api.nobitex.ir/market/stats"

    async def getCurrencys(self , nameCurrencys = False):
        url = self.urlCurrency
        
        if(nameCurrencys == False):
            async with httpx.AsyncClient() as client:
                pyload = await client.get(url=url)
        else:
            async with httpx.AsyncClient() as client:
                pyload = await client.get(url=url , params={"srcCurrency": nameCurrencys})
        
        text = json.loads(pyload.text)
        return text['stats']
    
    async def getNameCurrencys(self):
        
        name = {
            'Bitcoin' : 'btc',
            'Ethereum' : 'eth',
            'Binance Coin' : 'bnb',
            'Litecoin' : 'ltc',
            'Dogecoin' : 'doge',
            'TRON' : 'trx',
            'Ton' : 'ton',
            'Tether' : 'usdt',
            'Not' : 'not',
        }
        
        return name
    
    async def getNameCurrencysFa(self):
        
        name = {
            'Bitcoin' : 'بیت کوین',
            'Ethereum' : 'اتریوم',
            'Binance Coin' : 'بایننس کوین',
            'Litecoin' : 'لایت کوین',
            'Dogecoin' : 'دوج کوین',
            'TRON' : 'ترون',
            'Ton' : 'تون کوین',
            'Tether' : 'تتر',
            'Not' : 'نات کوین'
        }
        
        return name
    
    async def getNameCurrencysFaAll(self,nameCur:str):
        
        name = {
            "بیت کوین": "btc",
            "اتریوم": "eth",
            "ریپل": "xrp",
            "لایت کوین": "ltc",
            "کاردانو": "ada",
            "پولکادات": "dot",
            "بیت کوین کش": "bch",
            "ترون": "trx",
            "تتر": "usdt",
            "دلار": "usdt",
            "استلار": "xlm",
            "چین لینک": "link",
            "سولانا": "sol",
            "دوج کوین": "doge",
            "مونرو": "xmr",
            "تزوس": "xtz",
            "آوالانچ": "avax",
            "فانتوم": "ftm",
            "هارمونی": "one",
            "سند باکس": "sand",
            "ماتیک": "matic",
            "کازماس": "atom",
            "آیوتا": "miota",
            "نئو": "neo",
            "سنتیمنت": "snt",
            "بیت تورنت": "btt",
            "کیک": "cake",
            "فلو": "flow",
            "سوشی سواپ": "sushi",
            "هولوشین": "holo",
            "هو لو شین": "holo",
            "دنت": "dent",
            "آرور": "arvr",
            "ارور": "arvr",
            "بیت کوین گلد": "btg",
            "سنتیمنت": "snt",
        }
        
        return name[nameCur] if nameCur in name else False
    
    async def pyloadCurrency(self):
        
        Currencys = await self.getNameCurrencys()
                
        pyload = await self.getCurrencys(",".join(Currencys.values()))

        return pyload
    
    async def pyloadCurrencySingl(self,nameCode:str):
                     
        pyload = await self.getCurrencys(nameCode)

        return pyload
    
    async def getCurrencyToStrEn(self):
        
        Currencys = await self.getNameCurrencys()
        CurrencysFa = await self.getNameCurrencysFa()
        result = ""
        pyload = await self.pyloadCurrency()
        
        del Currencys['Tether']
        
        for i ,j in Currencys.items():
            arz = pyload[j + "-usdt"]
            
            Buy = float(arz['bestBuy'])
            PriceChange = arz['dayChange']
            
            nameFa = CurrencysFa[i]
            
            result += f"💵 {nameFa} : {Buy:,} دلار\n"
        
        return result
    
    async def getCurrencyToStrFa(self):
    
        Currencys = await self.getNameCurrencys()
        CurrencysFa = await self.getNameCurrencysFa()
        result = ""
        pyload = await self.pyloadCurrency()
        
        for i ,j in Currencys.items():
            arz = pyload[j + "-rls"]
            
            Buy = int(int(str(arz['bestBuy']).split('.')[0]) / 10)
            PriceChange = arz['dayChange']
            
            nameFa = CurrencysFa[i]
            
            result += f"💰 {nameFa} : {Buy:,} تومان\n"
        
        return result
    
    async def getCurrencyToStrSinglFa(self,nameCurrency:str):
    
        CurrencysFa = await self.getNameCurrencysFaAll(nameCurrency)
        
        if CurrencysFa == False:
            return False
        
        nameCode = CurrencysFa
        
        pyload = await self.pyloadCurrencySingl(nameCode)
        
        arz = pyload[nameCode + "-rls"]
        
        Buy = int(int(str(arz['bestBuy']).split('.')[0]) / 10)
        PriceChange = arz['dayChange']
        
        
        result = f"💰 {Buy:,} تومان 「{PriceChange}%」"
        
        return result
    
    async def getCurrencyToStrSinglEn(self , nameCurrency:str):
        
        CurrencysFa = await self.getNameCurrencysFaAll(nameCurrency)
        
        if CurrencysFa == False:
            return False
        
        nameCode = CurrencysFa

        if nameCode == "usdt":
            return ""
        
        pyload = await self.pyloadCurrencySingl(nameCode)
        
        arz = pyload[nameCode + "-usdt"]
        
        Buy = float(arz['bestBuy'])
        PriceChange = arz['dayChange']
        
        
        result = f"💵 {Buy:,} دلار 「{PriceChange}%」"
        
        return result
    
    
Currency = Currency()