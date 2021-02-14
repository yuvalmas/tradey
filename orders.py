import pyodbc
import requests
import json
import time
import os
from data_from_api import *
from db_inserts import *
import discord
from discord.ext import commands
from discord import Embed
from Discord_embeds import *
from db_inserts import *
from datetime import datetime
import random
from discord.ext.commands import CommandNotFound

# Create a client
client = discord.Client()
# Create a prefix
client = commands.Bot(command_prefix='!')
client.remove_command("help")

# On ready
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        return
    raise error

@client.command(pass_context=True)
async def start_orders(ctx):
    while True:
        conn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=DESKTOP-KLCEF57\SQLEXPRESS;"
            "Database=Stocks_Bot;"
            "Trusted_Connection=yes;")
        conn = pyodbc.connect(conn_str)
        # Create a cursor
        cursor = conn.cursor()

        # Get all symbols from db_connection
        Symbols = get_stock_names()
        # Go through all symbols
        for symbol in Symbols:
            # Get text
            text = get_data_from_api(symbol)
            # Load text into a json
            convertedDict = json.loads(text)
            # Save all data to local vars
            Symbol = convertedDict['Global Quote']['01. symbol']
            Open = convertedDict['Global Quote']['02. open']
            High = convertedDict['Global Quote']['03. high']    
            Low = convertedDict['Global Quote']['04. low']
            Price = convertedDict['Global Quote']['05. price']
            Volume = convertedDict['Global Quote']['06. volume']
            Latest_Trading_day = convertedDict['Global Quote']['07. latest trading day']
            Previous_Close = convertedDict['Global Quote']['08. previous close']
            Change = convertedDict['Global Quote']['09. change']
            Change_Percent = convertedDict['Global Quote']['10. change percent']
            cursor.execute("INSERT INTO dbo.TBL_API_GLOBAL_QUOTES VALUES (GETDATE(),?,?,?,?,?,?,?,?,?,?)", (Symbol, Open, High, Low, Price, Volume, Latest_Trading_day, Previous_Close, Change, Change_Percent))
            conn.commit()
            update_prices(symbol, Price)
            # Check for buy orders
            cursor.execute('''SELECT TOP(1000000) * FROM [dbo].[TBL_ORDERS]
            WHERE [Symbol] = ? AND [Status] = 0 AND [Price] >= ? AND [Order_Type] = ?''',(symbol, Price,'buy'))
            results = cursor.fetchall()
            results1 = []
            for result in results:
                results1.append(result)
            
            for i in range(len(results1)):
                New_Status = 1
                user = results1[i][2]
                wanted_price = results1[i][4]
                amount = results1[i][6]
                Transaction_Amount = float(Price)*float(amount)
                user = ctx.message.author.id
                user = client.get_user(user)
                await user.send(f'Your buy order for {symbol} was fullfilled with a price of ${Price}') 
                user = ctx.message.author.id
                cursor.execute('''UPDATE [Stocks_Bot].[dbo].[TBL_ORDERS]
                        SET 
                            [Status] = ?
                            ,[Last_Updated_Time] = GETDATE()
                            ,[Transaction_Price] = ?
                            ,[Transaction_Amount] = ?
                        WHERE
                            [User] = ? AND [Status] = 0 AND [Symbol] = ? AND [Price] >= ? AND [Order_Type] = ?;''',(New_Status, Price, Transaction_Amount, user,symbol, Price, 'buy'))
                conn.commit()
                balances = get_balances(user)
                current_balance = balances[0]
                holding_balance = balances[1]
                new_balance = float(current_balance)-(float(Price)*amount)
                new_holding = float(holding_balance)-(float(wanted_price)*amount)
                cursor.execute('''UPDATE [Stocks_Bot].[dbo].[TBL_USER_BALANCE]
                    SET 
                        [Current_Balance] = ?
                        ,[Holding_Balance] = ?
                        ,[Last_Updated_Time] = GETDATE()
                    WHERE
                        [User] = ?;''', (new_balance, new_holding, user))
                cursor.commit()
                if(Check_user_owns(user, symbol)):
                    amount_owned = get_amount_owned(user, symbol)
                    new_amount = float(amount_owned)+float(amount)
                    average_price = (float(get_average_price(user, symbol))+float(Price))/2
                    cursor.execute('''UPDATE [Stocks_Bot].[dbo].[TBL_HOLDING]
                    SET 
                        [Amount] = ?
                        ,[Price_bought_at] = ?
                    WHERE
                        [User] = ? AND [Symbol] = ?;''', (new_amount, average_price, user, symbol))
                    conn.commit()
                else:
                    cursor.execute('''INSERT INTO [Stocks_Bot].[dbo].[TBL_HOLDING] ([User], Symbol, Price_bought_at, Amount, On_Hold, Fulfilled_date, Current_value)
                    VALUES  (?,?,?,?,?,GETDATE(), ?)''', (user, symbol, Price, amount,0,float(Price)*float(amount)))
                    conn.commit()
            # Check for sell orders
            cursor.execute('''SELECT TOP(1000000) * FROM [dbo].[TBL_ORDERS]
            WHERE [Symbol] = ? AND [Status] = 0 AND [Price] <= ? AND [Order_Type] = ?''',(symbol, Price,'sell'))
            results = cursor.fetchall()
            results1 = []
            for result in results:
                results1.append(result)
            
            for i in range(len(results1)):
                New_Status = 1
                user = results1[i][2]
                amount = results1[i][6]
                Transaction_Amount = float(Price)*float(amount)
                user = ctx.message.author.id
                user = client.get_user(user)
                await user.send(f'Your sell order for {symbol} was fullfilled with a price of ${Price}')   
                cursor.execute('''UPDATE [Stocks_Bot].[dbo].[TBL_ORDERS]
                        SET 
                            [Status] = ?
                            ,[Last_Updated_Time] = GETDATE()
                            ,[Transaction_Price] = ?
                            ,[Transaction_Amount] = ?
                        WHERE
                            [User] = ? AND [Status] = 0 AND [Symbol] = ? AND [Price] <= ? AND [Order_Type] = ?;''',(New_Status, Price, Transaction_Amount, user,symbol, Price, 'sell'))
                cursor.commit()
                balances = get_balances(user)
                current_balance = balances[0]
                holding_balance = balances[1]
                new_balance = float(current_balance)+(float(Price)*amount)
                cursor.execute('''UPDATE [Stocks_Bot].[dbo].[TBL_USER_BALANCE]
                    SET 
                        [Current_Balance] = ?
                        ,[Last_Updated_Time] = GETDATE()
                    WHERE
                        [User] = ?;''', (new_balance, user))
                conn.commit()
                info = get_stock_owned(user, symbol)
                new_amount = info[0]-amount
                new_hold = info[1]-amount
                cursor.execute('''UPDATE [Stocks_Bot].[dbo].[TBL_HOLDING]
                    SET 
                        [Amount] = ?
                        ,[On_Hold] = ?
                    WHERE
                        [User] = ? AND [Symbol] = ?;''', (new_amount, new_hold, user, symbol))
                cursor.commit()
            print(Symbol)
            time.sleep(180)
            

def update_prices(symbol, price):
    price = float(price)
    cursor.execute('''UPDATE TOP(10000) [Stocks_Bot].[dbo].[TBL_HOLDING] SET 
    [Current_value] = [Amount]*? WHERE [Symbol] = ?''', (price, symbol))
    cursor.commit()

client.run(os.environ.get("DISCORD-BOT-TOKEN"))