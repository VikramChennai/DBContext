-- Table for product_sales.csv
CREATE TABLE product_sales (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    quantity_bought INT,
    price DECIMAL(10, 2),
    category VARCHAR(50),
    discount VARCHAR(10),
    supplier VARCHAR(255),
    sold_date DATE
);

-- Table for product_sales_2.csv
CREATE TABLE product_sales_2 (
    id INT PRIMARY KEY,
    prod_name VARCHAR(255),
    qty_purchase INT,
    unit_price DECIMAL(10, 2),
    prod_category VARCHAR(50),
    disc_percent INT,
    vendor VARCHAR(255),
    purchase_date DATE
);

-- Table for full_name.csv
CREATE TABLE stock_prices_full_name (
    Date DATE PRIMARY KEY,
    FACEBOOK DECIMAL(10, 2),
    GOOGLE DECIMAL(10, 2),
    APPLE DECIMAL(10, 2),
    TESLA DECIMAL(10, 2)
);

-- Table for ticker.csv
CREATE TABLE stock_prices_ticker (
    Date DATE PRIMARY KEY,
    META DECIMAL(10, 2),
    GOOGL DECIMAL(10, 2),
    AAPL DECIMAL(10, 2),
    TSLA DECIMAL(10, 2)
);

-- Table for random_table.csv
CREATE TABLE random_product_data (
    A12X INT PRIMARY KEY,
    B_Y7 VARCHAR(255),
    Q9ZP INT,
    MTR34 DECIMAL(10, 2),
    NXM12 VARCHAR(50),
    ZXC89 VARCHAR(10),
    LPO21 VARCHAR(255),
    JDW99 DATE
);

-- Import data for product_sales table
COPY product_sales(product_id, product_name, quantity_bought, price, category, discount, supplier, sold_date)
FROM '/path/to/DBContext/test_data/similar_header_test/product_sales.csv'
DELIMITER ',' CSV HEADER;

-- Import data for product_sales_2 table
COPY product_sales_2(id, prod_name, qty_purchase, unit_price, prod_category, disc_percent, vendor, purchase_date)
FROM '/path/to/DBContext/test_data/similar_header_test/product_sales_2.csv'
DELIMITER ',' CSV HEADER;

-- Import data for stock_prices_full_name table
COPY stock_prices_full_name(Date, FACEBOOK, GOOGLE, APPLE, TESLA)
FROM '/path/to/DBContext/test_data/stock_price_test/full_name.csv'
DELIMITER ',' CSV HEADER;

-- Import data for stock_prices_ticker table
COPY stock_prices_ticker(Date, META, GOOGL, AAPL, TSLA)
FROM '/path/to/DBContext/test_data/stock_price_test/ticker.csv'
DELIMITER ',' CSV HEADER;

-- Import data for random_product_data table
COPY random_product_data(A12X, B_Y7, Q9ZP, MTR34, NXM12, ZXC89, LPO21, JDW99)
FROM '/path/to/DBContext/test_data/random_header_test/random_table.csv'
DELIMITER ',' CSV HEADER;
