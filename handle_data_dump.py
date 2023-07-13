import sqlite3
from datetime import datetime
# SOURCE: pandas tutorial: https://www.youtube.com/watch?v=Q_JilB0sKfg&ab_channel=DanLeeman
# SOURCE: python to pandas to sql: https://learn.microsoft.com/en-us/sql/machine-learning/data-exploration/python-dataframe-sql-server?view=sql-server-ver16
import pandas as pd

# create and connect to SQL database
connection = sqlite3.connect('sales_data.sqlite')
cursor = connection.cursor()

# use pandas to open and read the csv files
store_sales = pd.read_csv('store_sales.csv', header=0)
online_sales = pd.read_csv('online_sales.csv', header=0)

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

# Transactions is our joiner table
cursor.execute("""CREATE Table if not exists SalesTotals
                    (
                        id integer primary key,
                        product_id integer,
                        store_id integer,
                        'online?' boolean,
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

connection.commit()
connection.close()