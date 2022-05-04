from DataGenerator import Constants as const, DataGeneratorBot

def create_bots(ib):
    bots = []
    
    bots.append(DataGeneratorBot.DataGeneratorBot(ib, const.STOCK))
        
    return bots