import sqlite3
import pandas as pd
import logging
from ingestion_db import ingest_db

# --------------------------------------------------
# Logging
# --------------------------------------------------
logging.basicConfig(
    filename="logs/get_vendor_summary.log",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a"
)

# --------------------------------------------------
# Load CSVs into Database (ONLY ONCE)
# --------------------------------------------------
def load_csvs_to_db(conn):
    logging.info("Loading CSV files into database...")

    pd.read_csv("purchases.csv").to_sql("purchases", conn, if_exists="replace", index=False)
    pd.read_csv("purchase_prices.csv").to_sql("purchase_prices", conn, if_exists="replace", index=False)
    pd.read_csv("sales.csv").to_sql("sales", conn, if_exists="replace", index=False)
    pd.read_csv("vendor_invoice.csv").to_sql("vendor_invoice", conn, if_exists="replace", index=False)

    logging.info("CSV data loaded successfully.")

# --------------------------------------------------
# Create Vendor Summary
# --------------------------------------------------
def create_vendor_summary(conn):
    query = """
    WITH FreightSummary AS (
        SELECT
            VendorNumber,
            SUM(Freight) AS FreightCost
        FROM vendor_invoice
        GROUP BY VendorNumber
    ),

    PurchaseSummary AS (
        SELECT
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price AS ActualPrice,
            pp.Volume,
            SUM(p.Quantity) AS TotalPurchaseQuantity,
            SUM(p.Dollars) AS TotalPurchaseDollars
        FROM purchases p
        JOIN purchase_prices pp
            ON p.Brand = pp.Brand
        WHERE p.PurchasePrice > 0
        GROUP BY
            p.VendorNumber,
            p.VendorName,
            p.Brand,
            p.Description,
            p.PurchasePrice,
            pp.Price,
            pp.Volume
    ),

    SalesSummary AS (
        SELECT
            VendorNo,
            Brand,
            SUM(SalesQuantity) AS TotalSalesQuantity,
            SUM(SalesDollars) AS TotalSalesDollars,
            SUM(SalesPrice) AS TotalSalesPrice,
            SUM(ExciseTax) AS TotalExciseTax
        FROM sales
        GROUP BY VendorNo, Brand
    )

    SELECT
        ps.VendorNumber,
        ps.VendorName,
        ps.Brand,
        ps.Description,
        ps.PurchasePrice,
        ps.ActualPrice,
        ps.Volume,
        ps.TotalPurchaseQuantity,
        ps.TotalPurchaseDollars,
        ss.TotalSalesQuantity,
        ss.TotalSalesDollars,
        ss.TotalSalesPrice,
        ss.TotalExciseTax,
        fs.FreightCost
    FROM PurchaseSummary ps
    LEFT JOIN SalesSummary ss
        ON ps.VendorNumber = ss.VendorNo
        AND ps.Brand = ss.Brand
    LEFT JOIN FreightSummary fs
        ON ps.VendorNumber = fs.VendorNumber
    ORDER BY ps.TotalPurchaseDollars DESC;
    """

    return pd.read_sql_query(query, conn)

# --------------------------------------------------
# Clean Data
# --------------------------------------------------
def clean_data(df):
    df['Volume'] = df['Volume'].astype(float)
    df.fillna(0, inplace=True)

    df['VendorName'] = df['VendorName'].str.strip()
    df['Description'] = df['Description'].str.strip()

    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']

    df['ProfitMargin'] = df.apply(
        lambda x: (x['GrossProfit'] / x['TotalSalesDollars'] * 100)
        if x['TotalSalesDollars'] != 0 else 0,
        axis=1
    )

    df['StockTurnover'] = df.apply(
        lambda x: x['TotalSalesQuantity'] / x['TotalPurchaseQuantity']
        if x['TotalPurchaseQuantity'] != 0 else 0,
        axis=1
    )

    df['SalesToPurchaseRatio'] = df.apply(
        lambda x: x['TotalSalesDollars'] / x['TotalPurchaseDollars']
        if x['TotalPurchaseDollars'] != 0 else 0,
        axis=1
    )

    return df

# --------------------------------------------------
# Main Execution
# --------------------------------------------------
if __name__ == "__main__":

    conn = sqlite3.connect("inventory.db")

    load_csvs_to_db(conn)

    logging.info("Creating vendor summary table...")
    summary_df = create_vendor_summary(conn)
    logging.info("\n%s", summary_df.head())

    logging.info("Cleaning data...")
    clean_df = clean_data(summary_df)
    logging.info("\n%s", clean_df.head())

    logging.info("Ingesting vendor_sales_summary table...")
    ingest_db(clean_df, "vendor_sales_summary", conn)

    logging.info(" Data ingestion completed successfully.")
