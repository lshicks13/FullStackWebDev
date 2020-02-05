import psycopg2

conn = psycopg2.connect('dbname=mydb user=postgres')

cursor = conn.cursor()

# Open a cursor to perform database operations
cur = conn.cursor()

# drop any existing todos table
cur.execute("DROP TABLE IF EXISTS table1;")

cur.execute("DROP TABLE IF EXISTS table2;")

# (re)create the todos table
# (note: triple quotes allow multiline text in python)
cur.execute("""
  CREATE TABLE table1 (
    id serial PRIMARY KEY,
    description VARCHAR NOT NULL
  );
""")

cur.execute("""
  CREATE TABLE table2 (
    id serial PRIMARY KEY,
    completed VARCHAR NOT NULL
  );
""")

cursor.execute('INSERT INTO table2 (id, completed) VALUES (%s, %s);', (1, True))

SQL = 'INSERT INTO table2 (id, completed) VALUES (%(id)s, %(completed)s);'

data = {
  'id': 2,
  'completed': False
}
cursor.execute(SQL, data)

# commit, so it does the executions on the db and persists in the db
conn.commit()

cur.close()
conn.close()