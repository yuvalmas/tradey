import pyodbc

# Create a connection to the database
conn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=DESKTOP-KLCEF57\SQLEXPRESS;"
            "Database=Stocks_Bot;"
            "Trusted_Connection=yes;")
conn = pyodbc.connect(conn_str)

# Create a cursor
cursor = conn.cursor()

def Create_Order(user, symbol, price, limit, amount, order_type):
    cursor.execute('''INSERT INTO dbo.TBL_ORDERS (
        [User]
       ,[Order_Type]
       ,[Symbol]
       ,[Price]
       ,[Limit]
       ,[Amount]
       ,[Order_Date_Time]
       ,[Status])
      VALUES (?,?,?,?,?,?,GETDATE(),0)''',(user, order_type, symbol, price, limit, amount) )
    conn.commit()

def Create_User(user, name, current_balance, holding_balance):
  cursor.execute('''insert into dbo.TBL_USER_BALANCE VALUES (?,?,?,?,?,GETDATE(), GETDATE())''', (user, name, current_balance, holding_balance,current_balance))
  conn.commit()

# Check if User exists
def Check_User_Exists(user):
  cursor.execute('select CASE isnull(MAX([Record_ID]),0) WHEN  0 THEN 0 ELSE 1 END  FROM [Stocks_Bot].[dbo].[TBL_USER_BALANCE] WHERE   [User] = ?', (user))
  row = cursor.fetchone()
  exists = str(row)
  exists = exists.count('0')
  if (exists == 0):
    return True
  else:
    return False

def get_balances(user):
  cursor.execute('''  SELECT TOP (1000) 
       [Current_Balance]
      ,[Holding_Balance]
      ,[Total_Balance]
      ,[Last_Updated_Time]
  FROM [Stocks_Bot].[dbo].[TBL_USER_BALANCE] 
  WHERE [User] = ?''', (user))
  results = cursor.fetchall()
  balances = []

  for balance in results:
    balances.append(balance)
  
  final_balances = []
  final_balances.append(str(balances[0][0]))
  final_balances.append(str(balances[0][1]))
  final_balances.append(str(balances[0][2]))
  final_balances.append(str(balances[0][3]))
  return final_balances

def change_balance(user, new_balance):
  cursor.execute('''UPDATE [Stocks_Bot].[dbo].[TBL_USER_BALANCE]
  SET 
	[Holding_Balance] = ?
	,[Last_Updated_Time] = GETDATE()
WHERE
	[User] = ?;''', (new_balance, user))

def check_stock(symbol):
  cursor.execute('''SELECT TOP 1  * FROM [dbo].[TBL_API_GLOBAL_QUOTES]
                    WHERE [Symbol] = ?
                    ORDER BY [Time_Stamp] DESC''', (symbol))
  results = cursor.fetchall()
  results1 = []
  for result in results:
    results1.append(result)
  # 
  results2 = []
  # Time Stamp, Open, High, Low, price, Latest trading day, previous close, change percent 
  results2.append(str(results1[0][0]))
  results2.append(str(results1[0][2]))
  results2.append(str(results1[0][3]))
  results2.append(str(results1[0][4]))
  results2.append(str(results1[0][5]))
  results2.append(str(results1[0][7]))
  results2.append(str(results1[0][8]))
  results2.append(str(results1[0][9]))
  return results2

def get_stock_names():
  # Get a list of all stock symbols
  cursor.execute("SELECT TOP(1000) * FROM dbo.TBL_MD_SYMBOL_INDEX")
  results = cursor.fetchall()
  # Create an array to save symbols formatted correctly
  Array_Of_Symbols = []
  # Format all symbols and insert into a list
  for symbol in results:
      symbol = symbol[0]
      Array_Of_Symbols.append(symbol)
  
  return Array_Of_Symbols

def Check_user_owns(user,symbol):
  cursor.execute('select CASE isnull(MAX([Record_ID]),0) WHEN  0 THEN 0 ELSE 1 END  FROM [Stocks_Bot].[dbo].[TBL_HOLDING] WHERE   [User] = ? AND [Symbol] = ?', (user,symbol))
  row = cursor.fetchone()
  exists = str(row)
  exists = exists.count('0')
  if (exists == 0):
    return True
  else:
    return False

def get_amount_owned(user, symbol):
  cursor.execute('''SELECT TOP(1) [Amount] FROM [Stocks_Bot].[dbo].[TBL_HOLDING] WHERE [User] = ? AND [Symbol] = ?''',(user, symbol))
  results = cursor.fetchall()
  amount = []
  amount.append(results[0])
  return amount[0][0]

def get_average_price(user, symbol):
  cursor.execute('''SELECT TOP(1) [Price_bought_at] FROM [Stocks_Bot].[dbo].[TBL_HOLDING] WHERE [User] = ? AND [Symbol] = ?''',(user, symbol))
  results = cursor.fetchall()
  Price_bought_at = []
  Price_bought_at.append(results[0])
  return Price_bought_at[0][0]

def get_on_hold(user, symbol):
  cursor.execute('''SELECT TOP(1) [On_Hold] FROM [Stocks_Bot].[dbo].[TBL_HOLDING] WHERE [User] = ? AND [Symbol] = ?''',(user, symbol))
  results = cursor.fetchall()
  amount = []
  amount.append(results[0])
  return amount[0][0]

def change_onhold(user, symbol, amount):
  on_hold = get_on_hold(user, symbol)
  new_hold = float(amount) + float(on_hold)
  cursor.execute('''UPDATE [Stocks_Bot].[dbo].[TBL_HOLDING]
  SET 
	[On_Hold] = ?
WHERE
	[User] = ? AND [Symbol] = ?;''', (new_hold, user, symbol))
  conn.commit()

def get_stock_owned(user, symbol):
  cursor.execute('''SELECT TOP(1)  [Amount],[On_Hold] FROM [dbo].[TBL_HOLDING]
                    WHERE [Symbol] = ? AND [User] = ?''', (symbol, user))
  results = cursor.fetchall()
  results1 = []
  for result in results:
    results1.append(result)
  # 
  results = []
  results.append(results1[0][0])
  results.append(results1[0][1])

  return results


def update_balance(user):
  cursor.execute('''SELECT SUM(Current_value) FROM [Stocks_Bot].[dbo].[TBL_HOLDING] WHERE [User] = ?''',(user))
  results = cursor.fetchall()
  cursor.execute('''SELECT SUM(Current_Balance) FROM [Stocks_Bot].[dbo].[TBL_USER_BALANCE] WHERE [User] = ?''',(user))
  results1 = cursor.fetchall()
  cursor.execute('select CASE isnull(MAX([Current_value]),0) WHEN  0 THEN 0 ELSE 1 END  FROM [Stocks_Bot].[dbo].[TBL_HOLDING] WHERE   [User] = ?', (user))
  row = cursor.fetchone()
  exists = str(row)
  exists = exists.count('0')
  if (exists == 0):
    cursor.execute('''UPDATE [Stocks_Bot].[dbo].[TBL_USER_BALANCE]
    SET 
    [Total_Balance] = ?+?
    ,[Last_Updated_Time] = GETDATE()
  WHERE
    [User] = ?;''', (float(results1[0][0]),float(results[0][0]),user))
  conn.commit()
  if (exists==1):
    cursor.execute('''UPDATE [Stocks_Bot].[dbo].[TBL_USER_BALANCE]
    SET 
    [Total_Balance] = ?+?
    ,[Last_Updated_Time] = GETDATE()
  WHERE
    [User] = ?;''', (float(0),float(results1[0][0]),user))
    

def check_for_stocks(user):
  cursor.execute('select CASE isnull(MAX([Record_ID]),0) WHEN  0 THEN 0 ELSE 1 END  FROM [Stocks_Bot].[dbo].[TBL_HOLDING] WHERE   [User] = ?', (user))
  row = cursor.fetchone()
  exists = str(row)
  exists = exists.count('0')
  if (exists == 0):
    return True
  else:
    return False

def show_my_stocks(user):
  cursor.execute('''SELECT TOP (1000) [Symbol]
      ,[Price_bought_at]
      ,[Amount]
      ,[On_Hold]
      ,[Current_value]
  FROM [Stocks_Bot].[dbo].[TBL_HOLDING]
  WHERE 
	[User]=?''',(user) )

  results = cursor.fetchall()
  # Create an array to save stocks formatted correctly
  Stocks = []
  # Format all stocks and insert into a list
  for symbol in results:
      Stocks.append(symbol)
  return Stocks

def check_for_orders(user):
  cursor.execute('select CASE isnull(MAX([Record_ID]),0) WHEN  0 THEN 0 ELSE 1 END  FROM [Stocks_Bot].[dbo].[TBL_ORDERS] WHERE   [User] = ?', (user))
  row = cursor.fetchone()
  exists = str(row)
  exists = exists.count('0')
  if (exists == 0):
    return True
  else:
    return False

def show_my_orders(user, status, price):
  if (price == 'Price'):
    cursor.execute('''SELECT TOP (3) [Order_Type] 
        ,[Symbol]
        ,[Price]
        ,[Limit]
        ,[Amount]
        ,[Order_Date_Time]
    FROM [Stocks_Bot].[dbo].[TBL_ORDERS]
    WHERE 
    [User]=? AND [Status] = ?
    ORDER BY [Order_Date_Time] DESC''',(user, status) )
  else:
    cursor.execute('''SELECT TOP (3) [Order_Type] 
        ,[Symbol]
        ,[Transaction_Price]
        ,[Limit]
        ,[Amount]
        ,[Order_Date_Time]
    FROM [Stocks_Bot].[dbo].[TBL_ORDERS]
    WHERE 
    [User]=? AND [Status] = ?
    ORDER BY [Order_Date_Time] DESC''',(user, status) )

  results = cursor.fetchall()
  # Create an array to save stocks formatted correctly
  orders = []
  # Format all stocks and insert into a list
  for symbol in results:
      orders.append(symbol)
  return orders