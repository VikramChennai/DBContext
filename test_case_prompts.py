# Test Case 1
prompt_1 = """
I have two tables in my PostgreSQL database, 'product_sales' and 'product_sales_2', which both
contain data about product sales. Unfortunately, since they are from two
different vendors the column names don't exactly match up, but they both
have the same type of information. Please merge these tables into one, giving it
informative column names and some descriptions too.
"""

# Test Case 2
prompt_2 = """
I have two tables in my PostgreSQL database, 'product_sales' and 'random_table', which both
contain data about product sales. 'product_sales' has nice column names
but the column names for 'random_table' were lost and are completely
garbage. These two tables really have the same type of data and so should
be one table. Please merge these tables into one, giving it informative 
column names and some descriptions too.
"""

# Test Case 3
prompt_3 = """
I have two tables in my PostgreSQL database, 'full_name' and 'ticker', which both contain stock
price data for a bunch of stocks. Since these are from different data
providers, one of them has the stocks as the company names while the other
has it as the tickers. Can you combine these tables to be one table with
all of the price data.
"""
