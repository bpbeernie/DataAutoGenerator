from ibapi.contract import Contract
from Globals import Globals as gb
import logging
import os
import datetime
from DataGenerator import Constants as const
import pickle

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_filename = "logs/autoGenerate.log"
os.makedirs(os.path.dirname(log_filename), exist_ok=True)
formatter = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
file_handler = logging.FileHandler(log_filename, mode="a", encoding=None, delay=False)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

#Bot Logic
class DataGeneratorBot:
    
    def __init__(self, ib, symbol):
        self.ib = ib
        self.symbol = symbol
        self.reqId = gb.Globals.getInstance().getOrderId()
        
        self.barsize = 1
        self.data = {}

    def setup(self):
        self.contract = Contract()
        self.contract.symbol = self.symbol.upper()
        self.contract.secType = "STK"
        self.contract.exchange = "SMART"
        self.contract.currency = "USD"
        self.contract.primaryExchange = "ARCA"
        
        self.data = []

        queryTime = const.TEST_DATE.strftime("%Y%m%d 23:59:59")
        
        self.ib.reqHistoricalData(self.reqId, self.contract,queryTime,"1 D",str(self.barsize)+ " min","TRADES",1,1,False,[])


    def on_bar_update(self, reqId, bar, realtime):
        if reqId != self.reqId:
            return
        
        date = datetime.datetime.strptime(bar.date, '%Y%m%d  %H:%M:%S')
        
        self.data.append({
            "Date": date,
            "Open": bar.open,
            "Close": bar.close,
            "High": bar.high,
            "Low": bar.low})
        
    def historicalDataEnd(self,reqId):
        if reqId != self.reqId:
            return
        
        file_name = "GeneratedFiles/" + self.symbol.upper() + "_" + const.TEST_DATE.strftime("%Y-%m-%d") + ".pkl"
        
        f = open(file_name, "wb")
        pickle.dump(self.data, f)
        f.close()


    def updateStatus(self, orderID, status):
        pass

    def on_realtime_update(self, reqId, time, open_, high, low, close, volume, wap, count):
        pass
