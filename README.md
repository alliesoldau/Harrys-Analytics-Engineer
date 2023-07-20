# Harry's Analytics Engineer Coding Project

**_Allie's answers are in italics_**

## _Instructions for How to Run the Code_
   1. _Ensure you have Python3 downloaded on your local environment._
      * _[Link for How to Check Your Python Version](https://blog.amphy.com/how-to-check-python-version/)_
      * _[Link to Python Download Instructions](https://www.python.org/downloads/)_
   2. _Ensure you have Sqlite installed on your local enviornment. Use Sqlite version 3.39.5. I can't gauruntee it works with the latest version._
      * _[Link for How to Check Your Sqlite Version](https://database.guide/check-sqlite-version/)_
      * _[Link to Sqlite Download Instructions](https://www.sqlitetutorial.net/download-install-sqlite/)_
   3. _Run_ `python3 handle_data_dump.py` _in the root directory in the terminal._ 
      * _This will take the_ `online_sales.csv` _and_ `store_sales.csv` _files, clean out any rows that have problematic data, return that problem data in the terminal for the analyst to see, and parse the good data into 4 tables in the Sqlite file_ `sales_data.sqlite`.
      * _[Link for How to Run Python Commands in the Terminal](https://realpython.com/run-python-scripts/#:~:text=To%20run%20Python%20scripts%20with,see%20the%20phrase%20Hello%20World!)._
   4. _Run_ `python3 graphs.py` _in the root directory in the terminal._
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

|                |ASCII                          |HTML                         |
|----------------|-------------------------------|-----------------------------|
|Single backticks|`'Isn't this fun?'`            |'Isn't this fun?'            |
|Quotes          |`"Isn't this fun?"`            |"Isn't this fun?"            |
|Dashes          |`-- is en-dash, --- is em-dash`|-- is en-dash, --- is em-dash|

## Task

This exercise contains two sales datasets for a retailer, store level sales and online sales. **Your
task is to design a data pipeline that can handle fresh files dropped daily and to model that data
for Analysts to use.**

- Assuming the files are dropped daily and contain the past 7 days of data, how would you handle deduping the records to ensure we have the latest data?
    - Assuming that the new data is dropped every 7 days, and the data from the previous days has *not* changed since it was last input, I would scan the data base to see which of the dates already exist in our tables, and ignore any data that is assocaited with that date. This way, even if someone forgets for a few days, only the new data will be pushed to the database.
- What should happen if there are missing values or errors in the input data?
    - I removed all rows that had any cells with missing data in them and then reindexed the data. I output a table which includes the information from the rows with missing data, including the index number, so that an analyst can look at it manually and decide whether or not to fix the data and push through an updated csv file.
- What does the final table(s) look like that an Analyst could use to build reporting?
    - 4 tables:
        Products (
                    id,
                    SKU
                )
        Stores (
                    id,
                    name
                )
        StoreSales (
                    id,
                    product_id,
                    store_id,
                    date,
                    units,
                    dollars
                )
        OnlineSales (
                    id,
                    product_id,
                    date,
                    units,
                    dollars
                )
    - I also added in a simple graphical representation which can be seen by running graphs.py to demonstrate how some of the data would look if the analyst graphed it
- If we were to expand to more retailers how would your code scale to handling?
    - Adding new stores/products is as simple as dropping it into the data dump file. The code will scan the data to see if there are any stores/products that don't currently exist in our database, and if there is, it will create a new row in the stores/products table to represent that new store/product.
- If an analyst using these pipelines found questionable data how would you advise they QA/troubleshoot the pipeline?

Please provide your code and a brief write-up describing your design decisions and any
assumptions you made in completing this task.

## Assumptions
- Dollars/$ Sales always in USD.
- Column titles will remain the same between datadumps
- We can ignore timezone and assume it won't affect the date values
- The analyst will want to manually examine any questionable data before opting to push it into the database.
- We want to round all $ values to the $0.00 place. I used the built in rounding method for python. If we want more granularity we can simply increase the sigfigs when we round that float value.
- Online sales are store agnostic since that column is not in their csv.
- When new data is dumped, we can assume that any data that is from a date that we already dumped data from can be ignored. I opted to ignore all data from dates we already logged in an effort to keep the program less time intensive. If we wanted to manually comb through each line of the data to see if it's a duplicate of what we already have or not, I could also implement this.

## Definitions

- SKU - is the unique identifier of a product we sell
- Qty/Units - the number of physical units we sold
- Dollars/$ Sales - is the dollar amount collected
- Online Sales sold online at the retailer's website
