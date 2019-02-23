#import sqlite3
#import csv

#conn = sqlite3.connect('pokemon.db')
#conn.row_factory = sqlite3.Row

#c = conn.cursor()


#with open('csv/pokemon.csv') as csv_file:
#    csv_reader = csv.reader(csv_file, delimiter=';')
#    line_count = 0
#    for row in csv_reader:
#        if line_count != 0:
#            name = row[1]
#            nationalDex = row[2]
#            height = row[3]
#            weight = row[4]
#            baseExp = row[5]

#            parameters = (name,nationalDex,height,weight,baseExp)
#            c.execute("INSERT INTO pokemon (nameEN,nationalDex,height,weight,baseExp) VALUES (?,?,?,?,?)",parameters)
#            conn.commit()
#conn.close()

import pokepy

client = pokepy.V2Client()

pokemon = client.get_pokemon(658)
pokemonSpecies = client.get_pokemon_species(658)




print(pokemonSpecies[0].generation)

nationalDex = pokemon[0].id
kantoDex = 0
johtoDex = 0
hoennDex = 0
sinnohDex = 0
einallDex = 0
kalosDex = 0

nameEN = pokemonSpecies[0].names[2].name
nameDE = pokemonSpecies[0].names[5].name

type1 = pokemon[0].types[0].type.name
type2 = pokemon[0].types[1].type.name

generation = 0

species = 0

height = pokemon[0].height
weight = pokemon[0].weight

dexInfo = 0

statHP = pokemon[0].stats[5].base_stat
statAtk = pokemon[0].stats[4].base_stat
statDef = pokemon[0].stats[3].base_stat
statSpAtk = pokemon[0].stats[2].base_stat
statSpDef = pokemon[0].stats[1].base_stat
statSpd = pokemon[0].stats[0].base_stat

evYield = 0

catchRate = pokemonSpecies[0].capture_rate

baseFriendship = pokemonSpecies[0].base_happiness
baseExp = pokemon[0].base_experience

growthRate = 0
eggGroup = 0
eggCycles = 0
genderMale = 100 - (100/(pokemonSpecies[0].gender_rate*8))
genderFemale = 100/(pokemonSpecies[0].gender_rate*8)

genderDifference = pokemonSpecies[0].has_gender_differences