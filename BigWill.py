import discord
import ftx
import pandas as pd
import json
import time
import ta
import matplotlib.pyplot as plt
from math import *

sortandentr=open('valeurMarcher.txt','w+')

# prerequi nom ect... (api)
pairSymbol = 'ETH/USD'
fiatSymbol = 'USD'
cryptoSymbol = 'ETH'
accountName = 'RAYROB'
goOn = True

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

print(floor(3.65))

'''
print(df)
print(sqrt((sum((df["close"]-df.mean(axis=0)["close"])**2))/df.shape[0]))
print(df.std(axis=0)["close"])
df['mean']=pourecent(df['close'].iloc[-1],-5)
df['prix']=df['close'].iloc[-1]
plt.figure()
plt.plot(df['time'],df['close'])
plt.plot(df['time'],df['mean'])
plt.plot(df['time'],df['prix'])
plt.show()
print(df.std(axis=0))
somme=39

coin=somme/df['close'].iloc[-1]

def buycondition(df):
    derniere_valeur=df['close'].iloc[-1]

print(coin)
print(coin*pourecent(df['close'].iloc[-1],10))
print(somme-coin*pourecent(df['close'].iloc[-1],10))

'''
