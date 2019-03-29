import sqlite3
import os
from os import listdir
from os.path import isfile, join
from pathlib import Path



conn = sqlite3.connect('pokemon.db')
conn.row_factory = sqlite3.Row


c = conn.cursor()


#c.execute("""SELECT * FROM pokemon WHERE (regionID = 1 OR regionID = 2 OR regionID = 3 OR regionID = 4) AND hasMegaEvolution = 1 ORDER BY name ASC""")
c.execute("""SELECT * FROM pokemon ORDER BY name ASC""")
pokeData = c.fetchall()

i = 0
for pm in pokeData:

    # Renamer
    #try:
    #    os.rename("front/" + pm["name"] + "_Mega.gif", "front/" + str(pm["nationalDex"]) + "FNM.gif")
    #    print(pm["nationalDex"])
    #except: pass

    #try:
    #    os.rename("front/" + pm["name"] + "_Female.gif", "front/" + str(pm["nationalDex"]) + "FNF.gif")
    #    print(pm["nationalDex"])
    #except: pass

    #try:
    #    os.rename("front/" + pm["name"] + ".gif", "front/" + str(pm["nationalDex"]) + "FN.gif")
    #except: pass

    #try:
    #    os.rename("front/" + pm["name"] + "_Alola.gif", "front/" + str(pm["nationalDex"]) + "FNA.gif")
    #except: pass

    #try:
    #    os.rename("front/" + pm["name"] + "_M.gif", "front/" + str(pm["nationalDex"]) + "FN.gif")
    #except: pass

    # Form Checker
    #filePath1 = "ShinyAll/" + str(pm["nationalDex"]) + "FS.gif"
    #filePath2 = "ShinyAll/" + str(pm["nationalDex"]) + "FSL01.gif"
    #filePath3 = "ShinyAll/" + str(pm["nationalDex"]) + "FSL02.gif"
    #filePath4 = "ShinyAll/" + str(pm["nationalDex"]) + "FSL03.gif"

    #if os.path.isfile(filePath2) and os.path.isfile(filePath1): print(str(pm["nationalDex"]) + " = Wrong") 
    #if os.path.isfile(filePath3) and os.path.isfile(filePath1): print(str(pm["nationalDex"]) + " = Wrong") 
    #if os.path.isfile(filePath4) and os.path.isfile(filePath1): print(str(pm["nationalDex"]) + " = Wrong") 

    try: os.rename("NormalAll/" + str(pm["nationalDex"]) + "FN.gif", "NormalAll/" + str('{0:03d}'.format(pm["nationalDex"])) + "FN.gif")
    except: pass

    try: os.rename("NormalAll/" + str(pm["nationalDex"]) + "FNF.gif", "NormalAll/" + str('{0:03d}'.format(pm["nationalDex"])) + "FNF.gif")
    except: pass

    try: os.rename("NormalAll/" + str(pm["nationalDex"]) + "FNM.gif", "NormalAll/" + str('{0:03d}'.format(pm["nationalDex"])) + "FNM.gif")
    except: pass

    try: os.rename("NormalAll/" + str(pm["nationalDex"]) + "FNM1.gif", "NormalAll/" + str('{0:03d}'.format(pm["nationalDex"])) + "FNM1.gif")
    except: pass

    try: os.rename("NormalAll/" + str(pm["nationalDex"]) + "FNM2.gif", "NormalAll/" + str('{0:03d}'.format(pm["nationalDex"])) + "FNM2.gif")
    except: pass

    try: os.rename("NormalAll/" + str(pm["nationalDex"]) + "FNA.gif", "NormalAll/" + str('{0:03d}'.format(pm["nationalDex"])) + "FNA.gif")
    except: pass

    try: os.rename("ShinyAll/" + str(pm["nationalDex"]) + "FS.gif", "ShinyAll/" + str('{0:03d}'.format(pm["nationalDex"])) + "FS.gif")
    except: pass

    try: os.rename("ShinyAll/" + str(pm["nationalDex"]) + "FSF.gif", "ShinyAll/" + str('{0:03d}'.format(pm["nationalDex"])) + "FSF.gif")
    except: pass

    try: os.rename("ShinyAll/" + str(pm["nationalDex"]) + "FSM.gif", "ShinyAll/" + str('{0:03d}'.format(pm["nationalDex"])) + "FSM.gif")
    except: pass

    try: os.rename("ShinyAll/" + str(pm["nationalDex"]) + "FSM1.gif", "ShinyAll/" + str('{0:03d}'.format(pm["nationalDex"])) + "FSM1.gif")
    except: pass

    try: os.rename("ShinyAll/" + str(pm["nationalDex"]) + "FSM2.gif", "ShinyAll/" + str('{0:03d}'.format(pm["nationalDex"])) + "FSM2.gif")
    except: pass

    try: os.rename("ShinyAll/" + str(pm["nationalDex"]) + "FSA.gif", "ShinyAll/" + str('{0:03d}'.format(pm["nationalDex"])) + "FSA.gif")
    except: pass

    for x in range(0,30):
        try: os.rename("ShinyAll/" + str(pm["nationalDex"]) + "FSL" + str('{0:02d}'.format(x)) + ".gif", "ShinyAll/" + str('{0:03d}'.format(pm["nationalDex"])) + "FSL" + str('{0:02d}'.format(x)) + ".gif")
        except: pass

        try: os.rename("NormalAll/" + str(pm["nationalDex"]) + "FNL" + str('{0:02d}'.format(x)) + ".gif", "NormalAll/" + str('{0:03d}'.format(pm["nationalDex"])) + "FNL" + str('{0:02d}'.format(x)) + ".gif")
        except: pass

    # DB Update

    #filePathFN = "NormalAll/" + str(pm["nationalDex"]) + "FN.gif"
    #filePathFNF = "NormalAll/" + str(pm["nationalDex"]) + "FNF.gif"
    #filePathFNM = "NormalAll/" + str(pm["nationalDex"]) + "FNM.gif"
    #filePathFNM1 = "NormalAll/" + str(pm["nationalDex"]) + "FNM1.gif"
    #filePathFNM2 = "NormalAll/" + str(pm["nationalDex"]) + "FNM2.gif"
    #filePathFNA = "NormalAll/" + str(pm["nationalDex"]) + "FNA.gif"

    #filePathFS = "ShinyAll/" + str(pm["nationalDex"]) + "FS.gif"
    #filePathFSF = "ShinyAll/" + str(pm["nationalDex"]) + "FSF.gif"
    #filePathFSM = "ShinyAll/" + str(pm["nationalDex"]) + "FSM.gif"
    #filePathFSM1 = "ShinyAll/" + str(pm["nationalDex"]) + "FSM1.gif"
    #filePathFSM2 = "ShinyAll/" + str(pm["nationalDex"]) + "FSM2.gif"
    #filePathFSA = "ShinyAll/" + str(pm["nationalDex"]) + "FSA.gif"

    #filePathMultiFormCheck1 = "NormalAll/" + str(pm["nationalDex"]) + "FNL01.gif"
    #filePathMultiFormCheck2 = "NormalAll/" + str(pm["nationalDex"]) + "FSL01.gif"

    #if not os.path.isfile(filePathMultiFormCheck1) and not os.path.isfile(filePathMultiFormCheck2): 

    #    parameters = (pm["nationalDex"],)
    #    c.execute("INSERT INTO sprites (nationalDex) VALUES (?)",parameters)
    #    conn.commit()

    #    if os.path.isfile(filePathFN):
    #        c.execute("UPDATE sprites SET spriteSheetHDFront = '" + str('{0:03d}'.format(pm["nationalDex"])) + "FN.gif' WHERE nationalDex = ?",parameters)
    #        conn.commit()

    #    if os.path.isfile(filePathFNF):
    #        c.execute("UPDATE sprites SET spriteSheetHDFrontFemale = '" + str('{0:03d}'.format(pm["nationalDex"])) + "FNF.gif' WHERE nationalDex = ?",parameters)
    #        conn.commit()

    #    if os.path.isfile(filePathFS):
    #        c.execute("UPDATE sprites SET spriteSheetHDFrontShiny = '" + str('{0:03d}'.format(pm["nationalDex"])) + "FS.gif' WHERE nationalDex = ?",parameters)
    #        conn.commit()

    #    if os.path.isfile(filePathFSF):
    #        c.execute("UPDATE sprites SET spriteSheetHDFrontFemaleShiny = '" + str('{0:03d}'.format(pm["nationalDex"])) + "FSF.gif' WHERE nationalDex = ?",parameters)
    #        conn.commit()


    #    if os.path.isfile(filePathFSM) or os.path.isfile(filePathFNM): 
    #        c.execute("INSERT INTO sprites (nationalDex,isMegaEvolution) VALUES (?,1)",parameters)
    #        conn.commit()

    #        if os.path.isfile(filePathFNM):
    #            c.execute("UPDATE sprites SET spriteSheetHDFront = '" + str('{0:03d}'.format(pm["nationalDex"])) + "FNM.gif' WHERE nationalDex = ?",parameters)
    #            conn.commit()

    #        if os.path.isfile(filePathFSM):
    #            c.execute("UPDATE sprites SET spriteSheetHDFrontShiny = '" + str('{0:03d}'.format(pm["nationalDex"])) + "FSM.gif' WHERE nationalDex = ?",parameters)
    #            conn.commit()

    #    if os.path.isfile(filePathFSM1) or os.path.isfile(filePathFNM1): 
    #        c.execute("INSERT INTO sprites (nationalDex,isMegaEvolution) VALUES (?,1)",parameters)
    #        conn.commit()

    #        if os.path.isfile(filePathFNM1):
    #            c.execute("UPDATE sprites SET spriteSheetHDFront = '" + str('{0:03d}'.format(pm["nationalDex"])) + "FNM1.gif' WHERE nationalDex = ?",parameters)
    #            conn.commit()

    #        if os.path.isfile(filePathFSM1):
    #            c.execute("UPDATE sprites SET spriteSheetHDFrontShiny = '" + str('{0:03d}'.format(pm["nationalDex"])) + "FSM1.gif' WHERE nationalDex = ?",parameters)
    #            conn.commit()

    #    if os.path.isfile(filePathFSM2) or os.path.isfile(filePathFNM2): 
    #        c.execute("INSERT INTO sprites (nationalDex,isMegaEvolution) VALUES (?,1)",parameters)
    #        conn.commit()

    #        if os.path.isfile(filePathFNM2):
    #            c.execute("UPDATE sprites SET spriteSheetHDFront = '" + str('{0:03d}'.format(pm["nationalDex"])) + "FNM2.gif' WHERE nationalDex = ?",parameters)
    #            conn.commit()

    #        if os.path.isfile(filePathFSM2):
    #            c.execute("UPDATE sprites SET spriteSheetHDFrontShiny = '" + str('{0:03d}'.format(pm["nationalDex"])) + "FSM2.gif' WHERE nationalDex = ?",parameters)
    #            conn.commit()

    #    if os.path.isfile(filePathFSA) or os.path.isfile(filePathFNA): 
    #        c.execute("INSERT INTO sprites (nationalDex,isAlolaForm) VALUES (?,1)",parameters)
    #        conn.commit()

    #        if os.path.isfile(filePathFNA):
    #            c.execute("UPDATE sprites SET spriteSheetHDFront = '" + str('{0:03d}'.format(pm["nationalDex"])) + "FNA.gif' WHERE nationalDex = ?",parameters)
    #            conn.commit()

    #        if os.path.isfile(filePathFSA):
    #            c.execute("UPDATE sprites SET spriteSheetHDFrontShiny = '" + str('{0:03d}'.format(pm["nationalDex"])) + "FSA.gif' WHERE nationalDex = ?",parameters)
    #            conn.commit()

    #else:

    #    for x in range(0,30):

    #        filePathMultiFormFN = "NormalAll/" + str(pm["nationalDex"]) + "FNL" + str('{0:02d}'.format(x)) + ".gif"
    #        filePathMultiFormFS = "ShinyAll/" + str(pm["nationalDex"]) + "FSL" + str('{0:02d}'.format(x)) + ".gif"

    #        if os.path.isfile(filePathMultiFormFN) or os.path.isfile(filePathMultiFormFS): 
    #            parameters = (pm["nationalDex"],)
    #            c.execute("INSERT INTO sprites (nationalDex, formNumber) VALUES (?, " + str(x) + ")",parameters)
    #            conn.commit()

    #            if os.path.isfile(filePathMultiFormFN):
    #                c.execute("UPDATE sprites SET spriteSheetHDFront = '" + str('{0:03d}'.format(pm["nationalDex"])) + "FNL" + str('{0:02d}'.format(x)) + ".gif' WHERE nationalDex = ? AND formNumber = " + str(x),parameters)
    #                conn.commit()

    #            if os.path.isfile(filePathMultiFormFS):
    #                c.execute("UPDATE sprites SET spriteSheetHDFrontFemale = '" + str('{0:03d}'.format(pm["nationalDex"])) + "FSL" + str('{0:02d}'.format(x)) + ".gif' WHERE nationalDex = ? AND formNumber = " + str(x),parameters)
    #                conn.commit()
    i+=1

print(i)







#c.execute("""SELECT * FROM pokemon WHERE (regionID = 1 OR regionID = 2 OR regionID = 3 OR regionID = 4) AND genderDifference = 1 ORDER BY name ASC""")
#pokeData = c.fetchall()

#i = 0
#for pm in pokeData:
#    try:
#        os.rename("GendersFemale/" + pm["name"] + "_Female.gif", "GendersFemale/" + str(pm["nationalDex"]) + "FNF.gif")
#        print(pm["nationalDex"])
#    except: print("Error: " + pm["name"])
#    i+=1

#print(i)



#parameters = (2,)
#c.execute("""SELECT * FROM pokemon WHERE regionID = 1 OR regionID = 2 OR regionID = 3 OR regionID = 4 ORDER BY nameEN ASC""")


#pokeData = c.fetchall()
#i=0

#onlyfiles = [f for f in listdir("spritesheets/Simplyfied/") if isfile(join("spritesheets/Simplyfied/", f))]



#for data in pokeData:
#    print(str(data["nationalDex"]) + "  " + data["nameEN"])
#    try:
#        if data["genderDifference"] == 1: 
#            #print(data["nameEN"] + "_Female")

            
#            #os.rename("spritesheets/Simplyfied/" + data["nameEN"] + ".gif", "spritesheets/Simplyfied/" + str(data["nationalDex"]) + "FN.gif")
#            i += 1
#        else:
#            #os.rename("spritesheets/Simplyfied/" + data["nameEN"] + ".gif", "spritesheets/Simplyfied/" + str(data["nationalDex"]) + "FN.gif")
#            i += 1
#    except: print("Error: " + data["nameEN"])

#print(str(i))

#conn.commit()

#conn.close()