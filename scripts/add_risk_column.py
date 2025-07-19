import psycopg2

conn = psycopg2.connect(
    dbname="moshoflo", user="admin", password="admin", host="localhost", port="5432"
)
cur = conn.cursor()

cur.execute("""
    ALTER TABLE trades ADD COLUMN risk_label TEXT;
""")

conn.commit()
cur.close()
conn.close()

print("'risk_label' column added to trades table.")