from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from Globals import Globals as gb

#Class for Interactive Brokers Connection
class IBApi(EWrapper,EClient):
    
    
    def __init__(self):
        EClient.__init__(self, self)
        self.closedPositions = []
        
    def addBots(self, bots):
        self._botList = bots
        
    # Historical Backtest Data
    def historicalData(self, reqId, bar):
        try:
            for bot in self._botList:
                bot.on_bar_update(reqId,bar,False)
        except Exception as e:
            print(e)
    # On Realtime Bar after historical data finishes
    def historicalDataUpdate(self, reqId, bar):
        try:
            for bot in self._botList:
                bot.on_bar_update(reqId,bar,True)
        except Exception as e:
            print(e)
    # On Historical Data End
    def historicalDataEnd(self, reqId, start, end):
        print("historicalDataEnd")
        print(reqId)
        try:
            for bot in self._botList:
                bot.historicalDataEnd(reqId)
        except Exception as e:
            print(e)
    # Get next order id we can use
    def nextValidId(self, nextorderId):
        gb.Globals.getInstance().orderId = nextorderId
        
            
    def error(self, id, errorCode, errorMsg):
        print(errorCode)
        print(errorMsg)
        

