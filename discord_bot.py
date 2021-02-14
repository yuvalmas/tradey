import discord
from discord.ext import commands
from discord import Embed
from Discord_embeds import *
from db_inserts import *
from datetime import datetime
import random
from discord.ext.commands import CommandNotFound
import os

# Create a client
client = discord.Client()
# Create a prefix
client = commands.Bot(command_prefix='!')
# Remove the default help command
client.remove_command("help")
# On ready
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_command_error(ctx, error):
    await ctx.send("Command does not exist please use !help to see all avaliable commands")
    if isinstance(error, CommandNotFound):
        return
    raise error

# Help command
@client.command(pass_context=True)
async def help(ctx, command='general'):
    user = ctx.message.author.id
    if (command == 'general'):
        await ctx.send(embed=help_menu())  
    if (command == 'start'):
        embed=discord.Embed(title="START COMMAND", description='''Command:\n
                                                            `!start [name]`\n
                                                            Example:
                                                            `!start Yuval`''', color=0x001eff)
        embed.add_field(name="Params:", value="• Name: name of the user that will show up on the leaderboard(defaults to user{random number}).", inline=False)
        await ctx.send(embed=embed)  
    if (command == 'restart'):
        embed=discord.Embed(title="RESTART COMMAND", description='''Command:\n
                                                            `!restart [name]`\n
                                                            Example:
                                                            `!restart Yuval`''', color=0x001eff)
        embed.add_field(name="Params:", value="• Name: name of the user that will show up on the leaderboard(defaults to user{random number}).", inline=False)
        await ctx.send(embed=embed)  
    if (command == 'symbols'):
        embed=discord.Embed(title="SYMBOLS COMMAND", description='''Command:\n
                                                            `!symbols`\n
                                                            Example:
                                                            `!symbols`''', color=0x001eff)
        embed.add_field(name="Params:", value="• None", inline=False)
        await ctx.send(embed=embed) 
    if (command == 'view'):
        embed=discord.Embed(title="VIEW COMMAND", description='''Command:\n
                                                            `!view (symbol)`\n
                                                            Example:
                                                            `!view TSLA`''', color=0x001eff)
        embed.add_field(name="Params:", value="• Symbol: Symbol of the share to view stats", inline=False)
        await ctx.send(embed=embed) 
    if (command == 'leaderboard'):
        embed=discord.Embed(title="LEADERBOARD COMMAND", description='''Command:\n
                                                            `!leaderboard`\n
                                                            Example:
                                                            `!leaderboard`''', color=0x001eff)
        embed.add_field(name="Params:", value="• None", inline=False)
        await ctx.send(embed=embed) 
    if (command == 'show_balance'):
        embed=discord.Embed(title="SHOW BALANCE COMMAND", description='''Command:\n
                                                            `!show_balance`\n
                                                            Example:
                                                            `!show_balance`''', color=0x001eff)
        embed.add_field(name="Params:", value="• None", inline=False)
        await ctx.send(embed=embed) 
    if (command == 'my_stocks'):
        embed=discord.Embed(title="MY STOCKS COMMAND", description='''Command:\n
                                                            `!my_stocks`\n
                                                            Example:
                                                            `!my_stocks`''', color=0x001eff)
        embed.add_field(name="Params:", value="• None", inline=False)
        await ctx.send(embed=embed) 
    if (command == 'my_orders'):
        embed=discord.Embed(title="MY ORDERS COMMAND", description='''Command:\n
                                                            `!my_orders`\n
                                                            Example:
                                                            `!my_orders`''', color=0x001eff)
        embed.add_field(name="Params:", value="• None", inline=False)
        await ctx.send(embed=embed) 
    if (command == 'buy'):
        embed=discord.Embed(title="BUY COMMAND", description='''Command:\n
                                                            `!buy (symbol) (price) [amount] [limit]`\n
                                                            Example:
                                                            `!buy TSLA 900 2 4`''', color=0x001eff)
        embed.add_field(name="Params:", value='''• Symbol: Symbol of the share to buy. \n
                                                 • Price: Price the user wants to buy the share at.\n
                                                 • Amount: Amount of shares to buy.\n
                                                 • Limit: amount of days for the order before cancelling.''', inline=False)
        await ctx.send(embed=embed) 
    if (command == 'sell'):
        embed=discord.Embed(title="SELL COMMAND", description='''Command:\n
                                                            `!sell (symbol) (price) [amount] [limit]`\n
                                                            Example:
                                                            `!sell AAPL 150 2 4`''', color=0x001eff)
        embed.add_field(name="Params:", value='''• Symbol: Symbol of the share to sell. \n
                                                 • Price: Price the user wants to sell the share at.\n
                                                 • Amount: Amount of shares to sell.\n
                                                 • Limit: amount of days for the order before cancelling.''', inline=False)
        await ctx.send(embed=embed) 
    

# Show all avaliable symbols
@client.command(pass_context=True)
async def symbols(ctx):
    await ctx.send(embed=show_symbols())

# Start User
@client.command(pass_context=True)
async def start(ctx, name=f'user{random.randint(1,100000)}'):
    # Get user ID 
    user = str(ctx.message.author.id)
    # Check if user exists
    if (Check_User_Exists(user)):
        await ctx.send(embed=user_already_created())
    else:
        user = ctx.message.author.id
        current_balance = 10000
        holding_balance = 0
        Create_User(str(user),name, int(current_balance), int(holding_balance))
        await ctx.send(embed=Created_user(name, int(current_balance), int(holding_balance)))

# Restart command
@client.command(pass_context=True)
async def restart(ctx, name=f'user{random.randint(1,100000)}'):
    # Get user ID
    user = ctx.message.author.id
    # Check if user exists
    if (Check_User_Exists(user)):
        # Delete all of users data 
        cursor.execute('DELETE FROM [Stocks_Bot].[dbo].[TBL_ORDERS] WHERE [User] = ?', user)
        cursor.execute('DELETE FROM [Stocks_Bot].[dbo].[TBL_USER_BALANCE] WHERE [User] = ?', user)
        cursor.execute('DELETE FROM [Stocks_Bot].[dbo].[TBL_HOLDING] WHERE [User] = ?', user)
        conn.commit()
        # Start user again
        current_balance = 10000
        holding_balance = 0
        Create_User(str(user),name, int(current_balance), int(holding_balance))
        user = ctx.message.author.id
        user = client.get_user(user)
        await ctx.send(embed=Created_user(name, int(current_balance), int(holding_balance)))
    else:
        # User doesn't exist
        await ctx.send(embed=User_Doesnt_Exists())

# Create buy order command
@client.command(pass_context=True)
async def buy(ctx, symbol='QWE', price='-999999', amount='1', limit='1'):
    # Get user ID
    user = ctx.message.author.id
    # Check if all params are correct
    try:
        price = float(price)
        amount = int(amount)
        limit = int(limit)
        # Change the symbol to uppercase
        symbol = symbol.upper()
        if (symbol=='QWE' or price==-999999):
            await ctx.send(embed=not_enough_params())
        else:
            # Check if the price entered is less than 0
            if (price <= 0 ):
                await ctx.send(embed=price_too_low())
            else:
                # Check if the amount entered is less than 0
                if (amount <= 0):
                    await ctx.send(embed=amount_too_low())
                else:
                    # Check if the limit entered is less than 0
                    if (limit <= 0):
                        await ctx.send(embed=limit_too_low())
                    else:
                        # Check if user exists
                        if(Check_User_Exists(user)):
                            # Check if the symbol exists in the db
                            symbols = get_stock_names()
                            if symbol not in symbols:
                                await ctx.send(embed=symbol_not_in_system())
                            else:
                                # Get current balances of the user to check if he has enough cash
                                balances = get_balances(user)
                                current_balance = float(balances[0])
                                holding_balance = float(balances[1])
                                sum_of_order = int(price)*int(amount)
                                leftover = current_balance-holding_balance-sum_of_order
                                if (leftover >= 0):
                                    # Create the buy order
                                    order_type = 'buy'
                                    new_holding_balance = holding_balance + sum_of_order
                                    change_balance(user, new_holding_balance)
                                    Create_Order(str(user), symbol, price, limit, amount, order_type)
                                    user = ctx.message.author.id
                                    user = client.get_user(user)
                                    await ctx.send(embed=Buy_Order(symbol, price, limit, amount))
                                else:
                                    user = ctx.message.author.id
                                    user = client.get_user(user)
                                    await ctx.send(embed=insufficient_funds())
                        else:
                            user = ctx.message.author.id
                            user = client.get_user(user)
                            await ctx.send(embed=User_Doesnt_Exists())
    except ValueError:
        await ctx.send(embed=invalid_params())

# Create sell order command
@client.command(pass_context=True)
async def sell(ctx, symbol='QWE', price='-999999', amount='1', limit='1'):
    # Check if all params are entered correctly
    try:
        price = float(price)
        amount = int(amount)
        limit = int(limit)
        symbol = symbol.upper()
        if (symbol=='QWE' or price==999999):
            await ctx.send(embed=not_enough_params())
        else:
            symbols = get_stock_names()
            if symbol not in symbols:
                await ctx.send(embed=symbol_not_in_system())
            else:
                # Check if the price entered is less than 0
                if (price <= 0 ):
                    await ctx.send(embed=price_too_low())
                else:
                    # Check if the amount entered is less than 0
                    if (amount <= 0):
                        await ctx.send(embed=amount_too_low())
                    else:
                        # Check if the limit entered is less than 0
                        if (limit <= 0):
                            await ctx.send(embed=limit_too_low())
                        else:
                            # Get user ID
                            user = ctx.message.author.id
                            # Check if user exists
                            if(Check_User_Exists(user)):
                                try:
                                    # Check if the user has enough shares
                                    amount_owned = get_amount_owned(user, symbol)
                                    on_hold = get_on_hold(user, symbol)
                                    if (amount > amount_owned-on_hold):
                                        await ctx.send(f'You do not own enough shares of {symbol}')  
                                    else:
                                        # Create  a sell order
                                        order_type = 'sell'
                                        Create_Order(int(user), symbol, price, limit, amount, order_type)
                                        change_onhold(user, symbol, amount)
                                        await ctx.send(embed=Sell_Order(symbol, price, limit, amount))
                                except:
                                    await ctx.send(f'You do not own any shares of {symbol}')  
                            else:
                                await ctx.send(embed=User_Doesnt_Exists())
    except ValueError:
        await ctx.send(embed=invalid_params())

# Show Balance
@client.command(pass_context=True)
async def show_balance(ctx):
    # Get user ID
    user = str(ctx.message.author.id)
    if(Check_User_Exists(user)):
        update_balance(user)
        Balances = get_balances(user)
        user = ctx.message.author.id
        user = client.get_user(user)
        await ctx.send(embed=show_balances(Balances))
    else:
        await ctx.send(embed=User_Doesnt_Exists())

# View stock stats
@client.command(pass_context=True)
async def view(ctx, symbol='QWE'):
    symbol = symbol.upper()
    if (symbol=='QWE'):
        await ctx.send(embed=not_enough_params())    
    else:
        symbols = get_stock_names()
        if symbol not in symbols:
            await ctx.send(embed=symbol_not_in_system())
        else:
            stock = check_stock(symbol)
            await ctx.send(embed=view_stock(symbol, stock))

# show leaderboard
@client.command(pass_context=True)
async def leaderboard(ctx):
    # Update all users
    cursor.execute('''SELECT TOP(10000000) [User] FROM [Stocks_Bot].[dbo].[TBL_USER_BALANCE]
    ORDER BY [Total_Balance] DESC''')
    results = cursor.fetchall()
    for i in range(len(results)):
        update_balance(str(results[i][0]))
    # Find top 10 Users
    cursor.execute('''SELECT TOP(10) [Name], [Total_Balance] FROM [Stocks_Bot].[dbo].[TBL_USER_BALANCE]
    ORDER BY [Total_Balance] DESC''')
    results = cursor.fetchall()
    names = []
    amounts = []
    for i in range(len(results)):
        names.append(str(results[i][0]))
    for i in range(len(results)):
        amounts.append(str(results[i][1]))
    embed=discord.Embed(title="LEADERBOARD")
    for i in range(len(names)):
        embed.add_field(name=f"{i+1}. {names[i]}", value=f"${amounts[i]}", inline=False)
    await ctx.send(embed=embed)

# Show user's stocks
@client.command(pass_context=True)
async def my_stocks(ctx):
    user = str(ctx.message.author.id)
    if(Check_User_Exists(user)):
        if (check_for_stocks(user)):
            stocks = show_my_stocks(user)
            embed=discord.Embed(title="YOUR STOCKS", color=0x0400ff)
            for i in range(len(stocks)):
                embed.add_field(name=f"{stocks[i][0]}", value=f"Average Price:${stocks[i][1]} \n Amount: {stocks[i][2]}\n On Hold: {stocks[i][3]} \n Current Value:${stocks[i][4]}\n", inline=False)
                user = ctx.message.author.id
                user = client.get_user(user)
            await ctx.send(embed=embed)
        else:
            user = ctx.message.author.id
            user = client.get_user(user)
            await ctx.send(f'You do not own any shares')        
    else:
        await ctx.send(embed=User_Doesnt_Exists())

# Show user's orders
@client.command(pass_context=True)
async def my_orders(ctx):
    user = str(ctx.message.author.id)
    if(Check_User_Exists(user)):
        if (check_for_orders(user)):
            # Get current orders
            embed=discord.Embed(title="YOUR ORDERS", color=0x0400ff)
            # Current Orders
            orders = show_my_orders(user, 0, 'Price')
            if (len(orders) > 0):
                s = ''
                for i in range(len(orders)):
                    s = s + f'Order Type: {orders[i][0]}, Symbol: {orders[i][1]}, Price: ${orders[i][2]}, Limit: {orders[i][3]}, Amount: {orders[i][4]}, Date: {orders[i][5]}\n\n'
                embed.add_field(name=f"CURRENT ORDERS", value=s, inline=False)
            # Fullfilled orders
            orders = show_my_orders(user, 1, 'Transaction_Price')
            if (len(orders) > 0):
                s = ''
                for i in range(len(orders)):
                    s = s + f'Order Type: {orders[i][0]}, Symbol: {orders[i][1]}, Price: ${orders[i][2]}, Limit: {orders[i][3]}, Amount: {orders[i][4]}, Date: {orders[i][5]}\n\n'
                embed.add_field(name=f"FULLFILLED ORDERS", value=s, inline=False)
            # Cancelled orders
            orders = show_my_orders(user, 9, 'Price')
            if (len(orders) > 0):
                s = ''
                for i in range(len(orders)):
                    s = s + f'Order Type: {orders[i][0]}, Symbol: {orders[i][1]}, Price: ${orders[i][2]}, Limit: {orders[i][3]}, Amount: {orders[i][4]}, Date: {orders[i][5]}\n\n'
                embed.add_field(name=f"CANCELLED ORDERS", value=s, inline=False)
            user = ctx.message.author.id
            user = client.get_user(user)
            await ctx.send(embed=embed)
        else:
            user = ctx.message.author.id
            user = client.get_user(user)
            await ctx.send(f'You do not have any orders')  
        
    else:
        await ctx.send(embed=User_Doesnt_Exists())


client.run(os.environ.get("DISCORD-BOT-TOKEN"))