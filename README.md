# Harry's Analytics Engineer Coding Project

## Task

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

## Questions
- Is the Dollars/$ Sales *always* in USD?