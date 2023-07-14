import sqlite3
import pandas as pd
import collections
import matplotlib.pyplot as plt

connection = sqlite3.connect('sales_data.sqlite')
cursor = connection.cursor()

# grab the number of units sold per product for the store sales
cursor.execute("""SELECT product_id, units FROM StoreSales""")
store_sales = cursor.fetchall()

d = {}
products = []
for key, val in store_sales:
    d[key] = d.get(key, 0) + val
od = collections.OrderedDict(sorted(d.items()))
for key in od:
    products.append(key)
product_units_sold = ([[key, od[key]] for key in products])

df = pd.DataFrame(product_units_sold, columns=['Product', 'Units'])
df.plot(x='Product', y='Units', kind='bar', title='Store Sales')	

# grab the number of units sold per product for the online sales
cursor.execute("""SELECT product_id, units FROM OnlineSales""")
online_sales = cursor.fetchall()

b = {}
online_products = []
for key, val in online_sales:
    b[key] = b.get(key, 0) + val
ob = collections.OrderedDict(sorted(b.items()))
for key in ob:
    online_products.append(key)
product_units_sold_online= ([[key, ob[key]] for key in online_products])

bf = pd.DataFrame(product_units_sold_online, columns=['Product', 'Units'])
bf.plot(x='Product', y='Units', kind='bar', title='Online Sales')	

plt.show()

connection.commit()
connection.close()