import pyodbc
from db_inserts import *
import time

conn_str = ("Driver={SQL Server Native Client 11.0};"
            "Server=DESKTOP-KLCEF57\SQLEXPRESS;"
            "Database=Stocks_Bot;"
            "Trusted_Connection=yes;")
conn = pyodbc.connect(conn_str)
# Create a cursor
cursor = conn.cursor()

def check_buy_limits():
    cursor.execute("""
    BEGIN
            IF EXISTS (SELECT 1 FROM [tempdb].[INFORMATION_SCHEMA].[TABLES] WHERE [TABLE_NAME] LIKE '#Temp_TBL_ORDERS%')
                BEGIN
                    PRINT 'AAA'
                    DROP TABLE #Temp_TBL_ORDERS
                END
            CREATE TABLE #Temp_TBL_ORDERS(
                    [User]						Nvarchar(50),
                    [Total_Holding_Balance]		Decimal(15,4))


            INSERT #Temp_TBL_ORDERS(
                    [User],
                    [Total_Holding_Balance])
            SELECT 
                [User],
                SUM(([dbo].[TBL_ORDERS].[Price] * [dbo].[TBL_ORDERS].[Amount]))
            FROM
                [dbo].[TBL_ORDERS]
            WHERE 
                DATEADD(D,[dbo].[TBL_ORDERS].Limit,[dbo].[TBL_ORDERS].Order_Date_Time) < GETDATE() 
                AND
                [dbo].[TBL_ORDERS].[Status] = 0		
                AND
                [dbo].[TBL_ORDERS].[Order_Type] = 'buy'
            GROUP BY
                [User]
        
            UPDATE [dbo].[TBL_USER_BALANCE]
                SET
                    [Holding_Balance] = [Holding_Balance] - #Temp_TBL_ORDERS.Total_Holding_Balance
                FROM
                    [dbo].[TBL_USER_BALANCE] JOIN #Temp_TBL_ORDERS ON
                    [dbo].[TBL_USER_BALANCE].[User] = #Temp_TBL_ORDERS.[User]

        
                UPDATE [Stocks_Bot].[dbo].[TBL_ORDERS] 
                SET 
                    [Status] = 9
                    ,[Last_Updated_Time] = GETDATE()
                WHERE 
                    DATEADD(D,[dbo].[TBL_ORDERS].Limit,[dbo].[TBL_ORDERS].Order_Date_Time) < GETDATE() 
                    AND
                    [dbo].[TBL_ORDERS].[Status] = 0			


            SELECT * FROM #Temp_TBL_ORDERS
        END""")
    conn.commit()

def check_sell_limits():
    Symbols = get_stock_names()
    for symbol in Symbols:
        cursor.execute("""
        BEGIN

            
            IF EXISTS (SELECT 1 FROM [tempdb].[INFORMATION_SCHEMA].[TABLES] WHERE [TABLE_NAME] LIKE '#Temp_TBL_ORDERS%')
                BEGIN
                    PRINT 'AAA'
                    DROP TABLE #Temp_TBL_ORDERS
                END
            CREATE TABLE #Temp_TBL_ORDERS(
                    [User]						Nvarchar(50),
                    [Total_Holding_Shares]		Decimal(15,4))


            INSERT #Temp_TBL_ORDERS(
                    [User],
                    [Total_Holding_Shares])
            SELECT 
                [User],
                SUM(([dbo].[TBL_ORDERS].[Amount]))
            FROM
                [dbo].[TBL_ORDERS]
            WHERE 
                DATEADD(D,[dbo].[TBL_ORDERS].Limit,[dbo].[TBL_ORDERS].Order_Date_Time) < GETDATE() 
                AND
                [dbo].[TBL_ORDERS].[Status] = 0		
                AND
                [dbo].[TBL_ORDERS].[Order_Type] = 'sell'
            GROUP BY
                [User]
        
            UPDATE [dbo].[TBL_HOLDING]
                SET
                    [On_Hold] = [On_Hold] - #Temp_TBL_ORDERS.Total_Holding_Shares
                FROM
                    [dbo].[TBL_HOLDING] JOIN #Temp_TBL_ORDERS ON
                    [dbo].[TBL_HOLDING].[User] = #Temp_TBL_ORDERS.[User]
                WHERE 
                    [dbo].[TBL_HOLDING].[Symbol] = ?

        
                UPDATE [Stocks_Bot].[dbo].[TBL_ORDERS] 
                SET 
                    [Status] = 9
                    ,[Last_Updated_Time] = GETDATE()
                WHERE 
                    DATEADD(D,[dbo].[TBL_ORDERS].Limit,[dbo].[TBL_ORDERS].Order_Date_Time) < GETDATE() 
                    AND
                    [dbo].[TBL_ORDERS].[Status] = 0			


            SELECT * FROM #Temp_TBL_ORDERS
        END""",(symbol))
    conn.commit()

while True:
    check_sell_limits()
    time.sleep(1)
    check_buy_limits()
    time.sleep(1)   
