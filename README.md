# Harry's Analytics Engineer Coding Project

**_Allie's answers are in italics_**

## _Instructions for How to Run the Code_
1. _Ensure you have Python3 downloaded on your local environment._
    * _[Link for How to Check Your Python Version](https://blog.amphy.com/how-to-check-python-version/)_
    * _[Link to Python Download Instructions](https://www.python.org/downloads/)_
2. _Ensure you have Sqlite installed on your local enviornment. Use Sqlite version 3.39.5. I can't gauruntee it works with the latest version._
    * _[Link for How to Check Your Sqlite Version](https://database.guide/check-sqlite-version/)_
    * _[Link to Sqlite Download Instructions](https://www.sqlitetutorial.net/download-install-sqlite/)_
3. _Ensure you have pandas installed on your local environment._
    * _Run_ `pip install pandas` _in the terminal._
4. _Ensure you have matplotlib installed on your local environment._
    * _[Link to matplotlib Installation Guide](https://matplotlib.org/stable/users/installing/index.html)_
5. _Run_ `python3 handle_data_dump.py` _in the root directory in the terminal._ 
    * _This will take the_ `online_sales.csv` _and_ `store_sales.csv` _files, clean out any rows that have problematic data, return that problem data in the terminal for the analyst to see, and parse the good data into 4 tables in the Sqlite file_ `sales_data.sqlite`.
    * _[Link for How to Run Python Commands in the Terminal](https://realpython.com/run-python-scripts/#:~:text=To%20run%20Python%20scripts%20with,see%20the%20phrase%20Hello%20World!)._
6. _Run_ `python3 graphs.py` _in the root directory in the terminal._
    * _This will create 2 pop-up graphs to demonstrate to demonstrate what an analyst could do with the data. The graphs have a tendancy to populate on a different monitor, so you may need to check your laptop and any external monitors for the pop-up._

## _Database Configuration_

* _The database consists of 4 tables as described below:_
    * **_Products_**
        * _All stores are associated with a unique id to make it easier to reference them_
    * **_Stores_**
        * _All products are associated with a unique id to make it easier to reference them_
    * **_StoreSales_**
        * _Joiner table which contains all the info about the store sales_
    * **_OnlineSales_**
        * _Joiner table which contains all the info about the online sales_

**Stores**
|id: int|name: string|
|--|--|
|1|'Store 1'|
|2|'Store 2'|
|3|'Store 3'|

**Products**
|id: int|SKU: string|
|--|--|
|1|'HP000235'|
|2|'HP000123'|
|3|'HP000234'|

**StoreSales**
|id: int|product_id: int| store_id: int|date:datetime|units:int|dollars:float|
|--|--|--|--|--|--|
|1|2|1|2022-12-04|997|9960.03|
|2|2|1|2022-12-05|1120|11188.3|
|3|2|1|2022-12-06|1070|10689.3|

**OnlineSales**
|id: int|product_id:int|date:datetime|units:int|dollars:float|
|--|--|--|--|--|
|1|2|2022-07-31|263|2627.37|
|2|2|2022-08-01|259|2587.41|
|3|2|2022-08-02|241|2407.59|

## Task

_My write-up is available through this [Google-Doc link](https://docs.google.com/document/d/1-BhAF_mh0d_GT6BL1ioPGmc5mdbMPpzTuM3aHfKvf6I/edit?usp=sharing)_

This exercise contains two sales datasets for a retailer, store level sales and online sales. **Your
task is to design a data pipeline that can handle fresh files dropped daily and to model that data
for Analysts to use.**

- Assuming the files are dropped daily and contain the past 7 days of data, how would you handle deduping the records to ensure we have the latest data?
- What should happen if there are missing values or errors in the input data?
- What does the final table(s) look like that an Analyst could use to build reporting?
- If we were to expand to more retailers how would your code scale to handling?
- If an analyst using these pipelines found questionable data how would you advise they QA/troubleshoot the pipeline?

Please provide your code and a brief write-up describing your design decisions and any
assumptions you made in completing this task.

## Definitions

- SKU - is the unique identifier of a product we sell
- Qty/Units - the number of physical units we sold
- Dollars/$ Sales - is the dollar amount collected
- Online Sales sold online at the retailer's website
