import sqlite3
import os
from os import listdir
from os.path import isfile, join


conn = sqlite3.connect('pokemon.db')
conn.row_factory = sqlite3.Row


c = conn.cursor()


parameters = (2,)
c.execute("""SELECT * FROM pokemon WHERE regionID = 1 OR regionID = 2 OR regionID = 3 OR regionID = 4 ORDER BY nameEN ASC""")


pokeData = c.fetchall()
i=0

onlyfiles = [f for f in listdir("spritesheets/Simplyfied/") if isfile(join("spritesheets/Simplyfied/", f))]



for data in pokeData:
    print(str(data["nationalDex"]) + "  " + data["nameEN"])
    try:
        if data["genderDifference"] == 1: 
            #print(data["nameEN"] + "_Female")

            
            #os.rename("spritesheets/Simplyfied/" + data["nameEN"] + ".gif", "spritesheets/Simplyfied/" + str(data["nationalDex"]) + "FN.gif")
            i += 1
        else:
            #os.rename("spritesheets/Simplyfied/" + data["nameEN"] + ".gif", "spritesheets/Simplyfied/" + str(data["nationalDex"]) + "FN.gif")
            i += 1
    except: print("Error: " + data["nameEN"])

print(str(i))

conn.commit()

conn.close()