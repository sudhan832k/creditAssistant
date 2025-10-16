import sqlite3

# Connect to the database (or create it)
conn = sqlite3.connect("credit_customers.db")
cursor = conn.cursor()

# Create the table if it doesn't exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers (
    customer_id INTEGER PRIMARY KEY,
    customer_name TEXT NOT NULL,
    current_credit_limit REAL,
    payment_terms TEXT,
    credit_limit_increase_requested REAL,
    total_sales_12mo REAL,
    current_receivables REAL,
    current_receivable_status TEXT,
    payment_history TEXT,
    disputes INTEGER,
    credit_rating TEXT
)
""")

# Insert the three sample records
sample_data = [
    (1, 'Alpha Foods', 20000, 'Net 30', 5000, 400000, 20000, 'Current',
     '99% on-time; consistent early payments', 0, 'A+'),
    
    (2, 'Beta Traders', 25000, 'Net 60', 15000, 500000, 100000, 'Current',
     '90% on-time; few delays', 1, 'B'),
    
    (3, 'Crest Logistics', 15000, 'Net 30', 6000, 200000, 50000, '90+d overdue',
     '70% on-time; multiple late payments', 3, 'C-')
]

cursor.executemany("""
INSERT OR REPLACE INTO customers (
    customer_id, customer_name, current_credit_limit, payment_terms,
    credit_limit_increase_requested, total_sales_12mo, current_receivables,
    current_receivable_status, payment_history, disputes, credit_rating
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", sample_data)

# Commit changes and close connection
conn.commit()
conn.close()

print("Sample data loaded successfully.")
