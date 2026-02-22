import psycopg2

conn = psycopg2.connect("""
      host=master.44f7138e-e6e2-4298-bb33-b092cff9b5e6.c.dbaas.selcloud.ru
      dbname=tests
      user=postgress
      password=postgress
      port=5432
""")

cur = conn.cursor()
cur.execute('SELECT 40+2')

print(cur.fetchone())

cur.close()
conn.close()
