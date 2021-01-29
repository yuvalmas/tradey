import discord
from discord.ext import commands
from discord import Embed
from datetime import datetime

def User_Doesnt_Exists():
    embed=discord.Embed(title="USER DOESN'T EXIST", description="This user doesn't have an account linked to it. Please use the !start command to start the game", color=0xff2600)
    embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed

def Created_user(name, current_balance, holding_balance):
    embed=discord.Embed(title='USER CREATED', description='Your user has been created', color=0x00ff11)
    embed.add_field(name='Your Name', value=name, inline=True)
    embed.add_field(name='Starting Balance', value=f'${current_balance}', inline=False)
    embed.add_field(name='Balance On Hold', value=f'${holding_balance}', inline=False)
    embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed

def Buy_Order(symbol, price, limit, amount):
    embed=discord.Embed(title='BUY ORDER', description='Placed a buy order:', color=0x004cff)
    embed.set_thumbnail(url='https://th.bing.com/th/id/OIP.79wlR5KchuTGW2xTcEdRiwHaFj?pid=Api&rs=1%22')
    embed.add_field(name='Symbol', value=symbol, inline=True)
    embed.add_field(name='Price', value=f'${price}', inline=True)
    embed.add_field(name='Day Limit', value=limit, inline=True)
    embed.add_field(name='Amount', value=amount, inline=True)
    embed.add_field(name='Date Created' , value=datetime.now(), inline=True)
    embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed

def Sell_Order(symbol, price, limit, amount):
    embed=discord.Embed(title='SELL ORDER', description='Placed a sell order:', color=0xff0000)
    embed.set_thumbnail(url='https://th.bing.com/th/id/OIP.79wlR5KchuTGW2xTcEdRiwHaFj?pid=Api&rs=1%22')
    embed.add_field(name='Symbol', value=symbol, inline=True)
    embed.add_field(name='Price', value=f'${price}', inline=True)
    embed.add_field(name='Day Limit', value=limit, inline=True)
    embed.add_field(name='Amount', value=amount, inline=True)
    embed.add_field(name='Date Created' , value=datetime.now(), inline=True)
    embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed

def symbol_not_in_system():
    embed=discord.Embed(title="SYMBOL DOESN'T EXIST", description="This symbol is not in our system please try a different one. To see available symbols type !symbols. ", color=0xff0000)
    embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed

def show_symbols():
    embed=discord.Embed(title="SYMBOLS", description="At the moment we have 10 available symbols. \n TSLA, NVDA, AAPL, MSFT, AMZN, FB, GOOG, PYPL, INTC, AMD.", color=0xff00ea)
    embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed

def user_already_created():
    embed=discord.Embed(title="USER ALREADY EXISTS", description="Your user already exists. Please use the !help command to see more options or type !restart to reset your game.", color=0xff0000)
    embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed

def insufficient_funds():
    embed=discord.Embed(title="INSUFFICIENT FUNDS", description="Your account doesn't have enough balance to fulfill this buy order.", color=0xffdd00)
    embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed

def show_balances(Balances):
    embed=discord.Embed(title="BALANCE STATEMENT", color=0xd4ff00)
    embed.add_field(name="Cash", value=f'${Balances[0]}', inline=True)
    embed.add_field(name="Balance On Hold", value=f'${Balances[1]}', inline=False)
    embed.add_field(name="Net Worth", value=f'${Balances[2]}', inline=False)
    embed.add_field(name="Last Updated", value=Balances[3], inline=False)
    embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed

def view_stock(symbol, stock):
    embed=discord.Embed(title="STOCK STATS", color=0x001eff)
    embed.add_field(name="Symbol", value=symbol, inline=True)
    embed.add_field(name="Price", value=f'${stock[4]}', inline=True)
    embed.add_field(name="Time Stamp", value=stock[0], inline=True)
    embed.add_field(name="Open", value=f'${stock[1]}', inline=True)
    embed.add_field(name="High", value=f'${stock[2]}', inline=True)
    embed.add_field(name="Low", value=f'${stock[3]}', inline=True)
    embed.add_field(name="Previous Close", value=f'${stock[6]}', inline=True)
    embed.add_field(name="Last Trading Day", value=stock[5], inline=True)
    embed.add_field(name="Change Percent", value=stock[7], inline=True)
    embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed

def not_enough_params():
    embed=discord.Embed(title="NOT ENOUGH PARAMETERS", description="You didn't input enough parameters. Use !help to see all required parameters for each command.", color=0x00ff11)
    embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed

def help_menu():
    embed=discord.Embed(title="HELP MENU ", description='''List of all available commands. \n
                                                            To see how to use a command use
                                                            `!help  <command>`''', color=0x001eff)
    embed.add_field(name="Start Command", value="`!start [name]`", inline=False)
    embed.add_field(name="Restart Command", value="`!restart [name]`", inline=False)
    embed.add_field(name="Symbols Command", value="`!symbols`", inline=False)
    embed.add_field(name="View Command", value="`!view (symbol)`", inline=False)
    embed.add_field(name="Leaderboard Command", value="`!leaderboard`", inline=False)
    embed.add_field(name="Show Balance Command", value="`!show_balance`", inline=False)
    embed.add_field(name="My Stocks Command", value="`!my_stocks`", inline=False)
    embed.add_field(name="My Orders Command", value="`!my_orders`", inline=False)
    embed.add_field(name="Buy Command", value="`!buy (symbol) (price) [amount] [limit]`", inline=False)
    embed.add_field(name="Sell Command", value="`!sell (symbol) (price) [amount] [limit]`", inline=False)
    embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed

def price_too_low():
    embed=discord.Embed(title="UNVALID PARAMETER", description="You cannot use a number lower than 0 for the price. Use !help to see all required parameters", color=0xff0000)
    embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed

def amount_too_low():
    embed=discord.Embed(title="UNVALID PARAMETER", description="You cannot use a number lower than 0 for the amount. Use !help to see all required parameters", color=0xff0000)
    embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed

def limit_too_low():
    embed=discord.Embed(title="UNVALID PARAMETER", description="You cannot use a number lower than 0 for the limit. Use !help to see all required parameters", color=0xff0000)
    embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed

def my_stocks(stocks):
    embed=discord.Embed(title="YOUR STOCKS")
    for i in range(len(stocks)):
        embed.add_field(name=f"{stocks[i][0]}", value=f"Average Price:${stocks[i][1]} \n Amount: {stocks[i][2]}\n On Hold: {stocks[i][3]} \n Current Value:{stocks[i][4]}\n", inline=True)
        embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed

def invalid_params():
    embed=discord.Embed(title="UNVALID PARAMETER", description="Price, limit and amount have to be a number. use !help to learn about the required parameters", color=0xff0000)
    embed.set_footer(text="Bot created by Yuval Mashiach")
    return embed