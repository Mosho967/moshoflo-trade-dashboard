import psycopg2

conn = psycopg2.connect(
    dbname="moshoflo", user="admin", password="admin", host="localhost", port="5432"
)
cur = conn.cursor()
cur.execute("DELETE FROM trades;")
conn.commit()
cur.close()
conn.close()

print("All trades deleted!")
