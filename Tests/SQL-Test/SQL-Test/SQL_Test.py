import sqlite3

conn = sqlite3.connect('pokemon.db')
conn.row_factory = sqlite3.Row


c = conn.cursor()


parameters = (2,)
c.execute("""SELECT *,
evoNext.evoNextDex AS nextEvolution,
evoPrev.evoDex AS prevEvolution
FROM pokemon 
LEFT JOIN sprites ON pokemon.nationalDex = sprites.nationalDex
LEFT JOIN types AS typeA ON pokemon.typeID1 = typeA.id 
LEFT JOIN types AS typeB ON pokemon.typeID2 = typeB.id 
LEFT JOIN regions ON pokemon.regionID = regions.id 
LEFT JOIN evYieldTypes ON pokemon.evYieldTypeID = evYieldTypes.id
LEFT JOIN growthRates ON pokemon.growthRateID = growthRates.id
LEFT JOIN eggGroups ON pokemon.eggGroupID = eggGroups.id
LEFT JOIN evolutions AS evoNext ON pokemon.nationalDex = evoNext.evoDex
LEFT JOIN evolutions AS evoPrev ON pokemon.nationalDex = evoNext.evoNextDex
WHERE pokemon.nationalDex = ?""",parameters)


pokeData = c.fetchone()


print(pokeData['nameDE'])
print("Next Evo = " + str(pokeData["nextEvolution"]))
print("Prev Evo = " + str(pokeData["prevEvolution"]))

conn.commit()

conn.close()