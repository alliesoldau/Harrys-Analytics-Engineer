import sqlite3
import pandas as pd
import datetime

# create and connect to SQL database
connection = sqlite3.connect('sales_data.sqlite')
cursor = connection.cursor()

# use pandas to open and read the csv files
store_sales_raw = pd.read_csv('store_sales.csv', header=0)
online_sales_raw = pd.read_csv('online_sales.csv', header=0)
# drop any rows with empty cells
store_sales = store_sales_raw.dropna()
online_sales = online_sales_raw.dropna()
# create a seperate table for any dropped rows that analysts could manually examine and input once ammended
dropped_store_sales = store_sales_raw[~store_sales_raw.index.isin(store_sales.index)]
dropped_online_sales = online_sales_raw[~online_sales_raw.index.isin(online_sales.index)]

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

# grab the unique date values from online sales and store sales so that we can check our data to ignore these dates
cursor.execute("""SELECT date from StoreSales""")
store_sales_db_dates = cursor.fetchall()
store_sales_db_dates = [x[0] for x in store_sales_db_dates]

cursor.execute("""SELECT date from OnlineSales""")
online_sales_db_dates = cursor.fetchall()
online_sales_db_dates = [x[0] for x in online_sales_db_dates]
# filter out any dates that we already have logged in our database
# now we'll only update the database with any new data that was in the data dump
store_sales = store_sales[~store_sales['Day'].isin(store_sales_db_dates)]
online_sales = online_sales[~online_sales['Date'].isin(online_sales_db_dates)]

# grab the unique store names to check against existing database
cursor.execute("""SELECT name from Stores""")
all_stores = cursor.fetchall()
# grab all unique store values from the dumped data
stores = store_sales['Store'].unique()

# if any of the stores in the dumped data don't currently exist in the database, add them in
for row in stores:
    # ensure all stores are being stored as strings
    row = str(row)
    if (all_stores.count(row) == 0):
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
    # ensure all products are being stored as strings
    row = str(row)
    if (all_products.count(row) == 0):
        all_products.append(row)
        cursor.execute('INSERT INTO Products(SKU) VALUES (?)', (row,))

# input store sales into the StoreSales database
for index in range(len(store_sales)): 
    current_store_sale = []
    # I'm dealing with each column seperately so that I can double-check and clean the data indvidually as needed
    # ensure product name is being stored as a string
    product_name = str(store_sales.loc[index, 'Product'])
    # grab the product id
    cursor.execute('SELECT id FROM Products WHERE SKU=?', (product_name,))
    product_id = ((cursor.fetchall())[0])[0]
    current_store_sale.append(product_id)
    # grab the store id
    store_name = store_sales.loc[index, 'Store']
    cursor.execute('SELECT id FROM Stores WHERE name=?', (store_name,))
    store_id = ((cursor.fetchall())[0])[0]
    current_store_sale.append(store_id)
    # grab the date
    current_date_string = store_sales.loc[index, 'Day']
    current_store_sale.append(current_date_string)
    date_format = '%Y-%m-%d'
    # use try-except block to ensure that our date is datetime compatable
        # if it's not, add it to an array which will be fed back to our analyst so they can fix the data and continue the loop
    try:
        current_date = datetime.datetime.strptime(current_date_string, date_format)
    except: 
        dropped_store_sales.append(store_sales[index])
        continue
    # grab the units and ensure they're being strored as ints
    current_units = int(store_sales.loc[index, 'QTY'])
    current_store_sale.append(current_units)
    # grab the dollars, ensure it's a float, & round them to the nearest cent
    current_dollars = float(store_sales.loc[index, '$ Sales'])
    current_store_sale.append(round(current_dollars, 2))
    # make sure there are no errors with the code before inserting it into our database
        # if there is an error, append it to our dropped store sales for the analyst, and continue the loop
    if not isinstance(current_units, int) or not isinstance(current_dollars, float):
        dropped_store_sales.append(store_sales[index])
        continue
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

# input online sales into the OnlineSales database
for index in range(len(online_sales)): 
    current_online_sale = []
    # I'm dealing with each column seperately so that I can double-check and clean the data indvidually as needed
    # grab the product id and ensure it's being stored as a string
    product_name = str(online_sales.loc[index, 'Product'])
    cursor.execute('SELECT id FROM Products WHERE SKU=?', (product_name,))
    product_id = ((cursor.fetchall())[0])[0]
    current_online_sale.append(product_id)
    # grab the date and ensure it's in the correct format
    current_date_string = online_sales.loc[index, 'Date']
    current_online_sale.append(current_date_string)
    date_format = '%Y-%m-%d'
    # use try-except block to ensure that our date is datetime compatable
            # if it's not, add it to an array which will be fed back to our analyst so they can fix the data and continue the loop
    try:
        current_date = datetime.datetime.strptime(current_date_string, date_format)
    except: 
        dropped_online_sales.append(online_sales[index])
        continue
    # grab the units and ensure they're in int format
    current_units = int(online_sales.loc[index, 'Units'])
    current_online_sale.append(current_units)
    # grab the dollars, ensure they're floats, & round them to the nearest cent
    current_dollars = float(online_sales.loc[index, 'Dollars'])
    current_online_sale.append(round(current_dollars, 2))
     # make sure there are no errors with the code before inserting it into our database
        # if there is an error, append it to our dropped store sales for the analyst, and continue the loop
    if not isinstance(current_units, int) or not isinstance(current_dollars, float):
        dropped_online_sales.append(online_sales[index])
        continue
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

print('Please note that any rows that were COMPLETELY empty have been dropped.')
if len(dropped_store_sales) > 0:
    print('There are this many problematic rows in stores sales:', len(dropped_store_sales))
    print('These are the store sales that have missing/problematic data. Please review this data. Once it is cleaned up, you can re-upload it to this program to it will push the fixed data to the database:', dropped_store_sales )
else: print('All of the raw store sales data looks good!')
if len(dropped_online_sales > 0):
    print('There are this many problematic rows in online sales:', len(dropped_online_sales))
    print('These are the online sales that have missing/problematic data. Please review this data. Once it is cleaned up, you can re-upload it to this program to it will push the fixed data to the database:', dropped_online_sales )
else: print('All of the raw online sales data looks good!')    
print('All of your data has been handled.')    

connection.commit()
connection.close()