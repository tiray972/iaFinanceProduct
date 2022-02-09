import discord
import ftx
import pandas as pd
import json
import time
import ta
import matplotlib.pyplot as plt
from math import *

def truncate(n, decimals=0):
    r = floor(float(n)*10**decimals)/10**decimals
    return str(r)

def getBalance(myclient, coin):
    jsonBalance = myclient.get_balances()
    if jsonBalance == []: 
        return 0
    pandaBalance = pd.DataFrame(jsonBalance)
    if pandaBalance.loc[pandaBalance['coin'] == coin].empty: 
        return 0
    else: 
        return float(pandaBalance.loc[pandaBalance['coin'] == coin]['free'])

# prerequi nom ect... (api)
pairSymbol = 'ETH/USD'
fiatSymbol = 'USD'
cryptoSymbol = 'ETH'
accountName = 'RAYROB'
goOn = True
myTruncate = 3
i = 9
j = 21


client = ftx.FtxClient(
    api_key='uFsATrNMdGYEAKgg2HxXFzAWPep3aEHbY0NnaS0u',
    api_secret='ccEx9nZ1mSr_Y_26p-IcyG2eA0HC3zPRcmkxe4nM',
    subaccount_name=accountName
)
result = client.get_balances()
# fontion pour montrer ceux que represente une hausse tant de pourcent
# pour une baisse il faut indiquer le moins
def pourecent(nombre,val):
    return nombre + (nombre * val / 100)

data = client.get_historical_data(
    market_name=pairSymbol,
    resolution=3600,
    limit=1000,
    start_time=float(round(time.time()))-150*3600,
    end_time=float(round(time.time())))
df=pd.DataFrame(data)
actualPrice = df['close'].iloc[-1]
fiatAmount = getBalance(client, fiatSymbol)
cryptoAmount = getBalance(client, cryptoSymbol)
minToken = 5/actualPrice
print('coin price :',actualPrice, 'usd balance', fiatAmount, 'coin balance :',cryptoAmount)



def innitialisation(df):# premet de definir les colone que lon'nas besoin
	df['sma']=ta.trend.sma_indicator(df['close'], 8)
	df['sma5']=ta.trend.sma_indicator(df['close'], 10)

note=open('valeurMarcher.txt','r+')
k=note.read()

def achat(df,k):
	if df['sma5'].iloc[-1] < df['sma'].iloc[-1] and str(k[0])=='s' and df['close'].iloc[-1] < pourcent(float(k[1:]),-5) :
		note=open('valeurMarcher.txt','w+')
		note.write('e'+str(df['close'].iloc[-1]))	
		return True
	else:
		return False

		
def vente(df,k):
	if df['sma5'].iloc[-1] > df['sma'].iloc[-1] and k[0]=='e' and df['close'].iloc[-1] > pourcent(float(k[1:]),5) :
		note=open('valeurMarcher.txt','w+')
		note.write('s'+str(df['close'].iloc[-1]))	
		return True
	else:
		return False


innitialisation(df)
if achat(df, k):
    if float(fiatAmount) > 5:
        quantityBuy = truncate(float(fiatAmount)/actualPrice, myTruncate)
        buyOrder = client.place_order(
            market=pairSymbol, 
            side="buy", 
            price=None, 
            size=quantityBuy, 
            type='market')
        print("BUY", buyOrder)
    else:
        goOn = True
        print("If you  give me more USD I will buy more",cryptoSymbol) 
        messages="If you  give me more USD I will buy more"+str(cryptoSymbol) 
		
elif vente(df, k):
    if float(cryptoAmount) > minToken:
        sellOrder = client.place_order(
            market=pairSymbol, 
            side="sell", 
            price=None, 
            size=truncate(cryptoAmount, myTruncate), 
            type='market')
        print("SELL", sellOrder)
    else:
        goOn = True
        print("If you give me more",cryptoSymbol,"I will sell it")
        messages="If you give me more"+str(cryptoSymbol)+"I will sell it"
else :
    goOn = True
    print("No opportunity to take")
    messages="No opportunity to take"



