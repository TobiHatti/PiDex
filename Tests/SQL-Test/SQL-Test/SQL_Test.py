import sqlite3

conn = sqlite3.connect('pokemon.db')

c = conn.cursor()

#c.execute("""CREATE TABLE pokemon (
#            name text,
#            typeID integer
#           )""")

c.execute("""INSERT INTO pokemon""")

conn.commit()

conn.close()