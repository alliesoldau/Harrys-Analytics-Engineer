import sqlite3
from datetime import datetime
# SOURCE: pandas tutorial: https://www.youtube.com/watch?v=Q_JilB0sKfg&ab_channel=DanLeeman
# SOURCE: python to pandas to sql: https://learn.microsoft.com/en-us/sql/machine-learning/data-exploration/python-dataframe-sql-server?view=sql-server-ver16
import pandas as pd

# create and connect to SQL database
connection = sqlite3.connect('sales_data.sqlite')
cursor = connection.cursor()

# use pandas to open and read the csv files
store_sales_raw = pd.read_csv('store_sales.csv', header=0)
online_sales_raw = pd.read_csv('online_sales.csv', header=0)
# drop any rows with empty cells
store_sales = store_sales_raw.dropna()
online_sales = online_sales_raw.dropna()
# reset indexes after dropping rows
store_sales.reset_index(drop=True, inplace=True)
online_sales.reset_index(drop=True, inplace=True)

# create tables if they don't already exist --> this should only execute on initial run
# if this were a real life scenario I'd house this in a seperate file for safe keeping, but I'm leaving it here to make it easier to read the code and my process
cursor.execute("""CREATE Table if not exists Stores
                    (
                        id integer primary key,
                        name string
                    )
                """)

cursor.execute("""CREATE Table if not exists Products
                    (
                        id integer primary key,
                        SKU string
                    )
                """)

# StoreSales is a joiner table
cursor.execute("""CREATE Table if not exists StoreSales
                    (
                        id integer primary key,
                        product_id integer,
                        store_id integer,
                        date datetime,
                        units integer,
                        dollars float
                    )
                """)

# OnlineSales is a joiner table
cursor.execute("""CREATE Table if not exists OnlineSales
                    (
                        id integer primary key,
                        product_id integer,
                        date datetime,
                        units integer,
                        dollars float
                    )
                """)

# TO DO: deal with messy or errored data
# grab the unique store names to check against existing database
cursor.execute("""SELECT name from Stores""")
all_stores = cursor.fetchall()
# grab all unique store values from the dumped data
stores = store_sales['Store'].unique()
# if any of the stores in the dumped data don't currently exist in the database, add them in
for row in stores:
    if (isinstance(row, str) and all_stores.count(row) == 0):
        all_stores.append(row)
        cursor.execute('INSERT INTO Stores(name) VALUES (?)', (row,))

# grab the unique product names from the existing database
cursor.execute("""SELECT SKU from Products""")
all_products = cursor.fetchall()       
# grab all the unique products from both sales sources 
store_products = store_sales['Product'].unique()
online_products = online_sales['Product'].unique() # currently online stores don't specify the store name, but I'll keep this in in case that comes along in future data dump
# combine and remove any duplicates between both sales sources
products = list(set(online_products) | set(store_products))
# if any products in the dumped data don't currently exist in the database, add them in
for row in products:
    if (isinstance(row, str) and all_products.count(row) == 0):
        all_products.append(row)
        cursor.execute('INSERT INTO Products(SKU) VALUES (?)', (row,))

# TO DO: now i've created my base tables and i have to go through the actual transactions to create the joiner table
# TO DO: can't forget to clean the data, handle duplicates, double check that any data from previous days hasnt changed
    # and if it has, add that to the database/alert analysts

# Input store sales into the StoreSales database
for index in range(len(store_sales)): 
    current_store_sale = []
    # I'm dealing with each column seperately so that I can double-check and clean the data indvidually as needed
    # grab the product id
    product_name = store_sales.loc[index, 'Product']
    cursor.execute('SELECT id FROM Products WHERE SKU=?', (product_name,))
    product_id = ((cursor.fetchall())[0])[0]
    current_store_sale.append(product_id)
    # grab the store id
    store_name = store_sales.loc[index, 'Store']
    cursor.execute('SELECT id FROM Stores WHERE name=?', (store_name,))
    store_id = ((cursor.fetchall())[0])[0]
    current_store_sale.append(store_id)
    # grab the date
    current_date = store_sales.loc[index, 'Day']
    current_store_sale.append(current_date)
    # grab the units
    current_units = store_sales.loc[index, 'QTY']
    current_store_sale.append(current_units)
    # grab the dollars & round them to the nearest cent
    current_dollars = store_sales.loc[index, '$ Sales']
    current_store_sale.append(round(current_dollars, 2))
    # insert the sales into the stores sales table
    cursor.execute("""INSERT INTO StoreSales
                        ( 
                            product_id,
                            store_id,
                            date,
                            units,
                            dollars
                        )
                            VALUES (?,?,?,?,?)
                    """, current_store_sale)


# Input online sales into the OnlineSales database
for index in range(len(online_sales)): 
    current_online_sale = []
    # I'm dealing with each column seperately so that I can double-check and clean the data indvidually as needed
    # grab the product id
    product_name = online_sales.loc[index, 'Product']
    cursor.execute('SELECT id FROM Products WHERE SKU=?', (product_name,))
    product_id = ((cursor.fetchall())[0])[0]
    current_online_sale.append(product_id)
    # grab the date
    current_date = online_sales.loc[index, 'Date']
    current_online_sale.append(current_date)
    # grab the units
    current_units = online_sales.loc[index, 'Units']
    current_online_sale.append(current_units)
    # grab the dollars & round them to the nearest cent
    current_dollars = online_sales.loc[index, 'Dollars']
    current_online_sale.append(round(current_dollars, 2))
    # insert the sales into the stores sales table
    cursor.execute("""INSERT INTO OnlineSales
                        ( 
                            product_id,
                            date,
                            units,
                            dollars
                        )
                            VALUES (?,?,?,?)
                    """, current_online_sale)
    

connection.commit()
connection.close()