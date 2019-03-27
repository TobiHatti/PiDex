import sqlite3
import pokepy



#pokemon = client.get_pokemon(25)
#pokemonSpecies = client.get_pokemon_species(4)
#pokemonEvoChain = client.get_evolution_chain(1)
#pokemonGrowthRate = client.get_growth_rate(1)

#i = 0
#try:
#    while pokemonSpecies[0].pokedex_numbers[i].pokedex.name != None:
#        print(pokemonSpecies[0].pokedex_numbers[i].pokedex.name + " = " + str(pokemonSpecies[0].pokedex_numbers[i].entry_number))
#        i += 1
#except IndexError: pass


#pokedexTypes = list()
#isNewDex = True

#for j in range(1,803):
#    print("Checking Dex-ID: " + str(j))

#    if j%20 == 0: 
#        print("===== Current State: ====")
#        print(pokedexTypes)
#        print("=========================")

#    i = 0
#    try:
#        while client.get_pokemon_species(j)[0].pokedex_numbers[i].pokedex.name != None:

#            isNewDex = True

#            for x in range(0,len(pokedexTypes)):
#                if str(pokedexTypes[x]) == str(client.get_pokemon_species(j)[0].pokedex_numbers[i].pokedex.name): isNewDex = False

#            if isNewDex:
#                pokedexTypes.append(client.get_pokemon_species(j)[0].pokedex_numbers[i].pokedex.name)

#            i += 1
#    except: pass


#print(pokedexTypes)

conn = sqlite3.connect('pokemon.db')
conn.row_factory = sqlite3.Row
c = conn.cursor()

client = pokepy.V2Client()

eGr = 0

pokemonWithMega = (15,18,80,208,256,260,302,319,323,334,362,373,376,380,381,384,428,475,351,719,3,6,9,65,94,115,127,130,142,150,181,212,214,229,248,257,282,303,306,308,310,354,359,445,448,460)
for pm in pokemonWithMega:
    parameters = (pm,)
    print(pm)
    c.execute("UPDATE pokemon SET hasMegaEvolution = 1 WHERE nationalDex = ?",parameters)
    conn.commit()


pokemonEvoChain = client.get_evolution_chain(10)

pokemonSpecies = client.get_pokemon_species(pokemonEvoChain[0].chain.species.name)

#try:
#    for x in range(1,803):
#        print(x)
#        try:
#            pokemonEvoChain = client.get_evolution_chain(x)

#            for x1 in range(0,17):
#                try:

#                    pmFrom = pokemonEvoChain[0].chain.species.name
#                    pmTo = pokemonEvoChain[0].chain.evolves_to[x1].species.name

#                    pmFromDex = client.get_pokemon_species(pmFrom)[0].id
#                    pmToDex = client.get_pokemon_species(pmTo)[0].id

#                    try: pmMinLevel = pokemonEvoChain[0].chain.evolves_to[x1].evolution_details[0].min_level
#                    except: pmMinLevel = None

#                    try: pmEvoItem = pokemonEvoChain[0].chain.evolves_to[x1].evolution_details[0].item.name
#                    except: pmEvoItem = None

#                    print("From: " + pmFrom + " To: " + pmTo)
#                    print("From: " + str(pmFromDex) + " To: " + str(pmToDex))
#                    print("Min-Level: " + str(pmMinLevel))
#                    print("================================Item: " + str(pmEvoItem))

#                    parameters = (pmFromDex,pmToDex,pmMinLevel,pmEvoItem,)
#                    c.execute("INSERT INTO evolutions (evoDex, evoNextDex, evoNextItem,evoNextLevel) VALUES (?,?,?,?)",parameters)
#                    conn.commit()

                

#                except: pass

#                for x2 in range(0,17):
#                    try:
#                        pmFrom = pokemonEvoChain[0].chain.evolves_to[x1].species.name
#                        pmTo = pokemonEvoChain[0].chain.evolves_to[x1].evolves_to[x2].species.name

#                        pmFromDex = client.get_pokemon_species(pmFrom)[0].id
#                        pmToDex = client.get_pokemon_species(pmTo)[0].id

#                        try: pmMinLevel = pokemonEvoChain[0].evolves_to[x1].evolves_to[x2].evolution_details[0].min_level
#                        except: pmMinLevel = None

#                        try: pmEvoItem = pokemonEvoChain[0].evolves_to[x1].evolves_to[x2].evolution_details[0].item.name
#                        except: pmEvoItem = None

#                        print("From: " + pmFrom + " To: " + pmTo)
#                        print("From: " + str(pmFromDex) + " To: " + str(pmToDex))
#                        print("Min-Level: " + str(pmMinLevel))
#                        print("================================Item: " + str(pmEvoItem))

#                        parameters = (pmFromDex,pmToDex,pmMinLevel,pmEvoItem,)
#                        c.execute("INSERT INTO evolutions (evoDex, evoNextDex, evoNextItem,evoNextLevel) VALUES (?,?,?,?)",parameters)
#                        conn.commit()
#                    except: pass

#                    for x3 in range(0,17):
#                        try:
#                            pmFrom = pokemonEvoChain[0].chain.evolves_to[x1].evolves_to[x2].species.name
#                            pmTo = pokemonEvoChain[0].chain.evolves_to[x1].evolves_to[x2].evolves_to[x3].species.name

#                            pmFromDex = client.get_pokemon_species(pmFrom)[0].id
#                            pmToDex = client.get_pokemon_species(pmTo)[0].id

#                            try: pmMinLevel = pokemonEvoChain[0].chain.evolves_to[x1].evolves_to[x2].evolves_to[x3].evolution_details[0].min_level
#                            except: pmMinLevel = None

#                            try: pmEvoItem = pokemonEvoChain[0].chain.evolves_to[x1].evolves_to[x2].evolves_to[x3].evolution_details[0].item.name
#                            except: pmEvoItem = None

#                            print("From: " + pmFrom + " To: " + pmTo)
#                            print("From: " + str(pmFromDex) + " To: " + str(pmToDex))
#                            print("Min-Level: " + str(pmMinLevel))
#                            print("================================Item: " + str(pmEvoItem))

#                            parameters = (pmFromDex,pmToDex,pmMinLevel,pmEvoItem,)
#                            c.execute("INSERT INTO evolutions (evoDex, evoNextDex, evoNextItem,evoNextLevel) VALUES (?,?,?,?)",parameters)
#                            conn.commit()
#                        except: pass   

#                        for x4 in range(0,17):
#                            try:
#                                pmFrom = pokemonEvoChain[0].chain.evolves_to[x1].evolves_to[x2].evolves_to[x3].species.name
#                                pmTo = pokemonEvoChain[0].chain.evolves_to[x1].evolves_to[x2].evolves_to[x3].evolves_to[x4].species.name

#                                pmFromDex = client.get_pokemon_species(pmFrom)[0].id
#                                pmToDex = client.get_pokemon_species(pmTo)[0].id

#                                try: pmMinLevel = pokemonEvoChain[0].chain.evolves_to[x1].evolves_to[x2].evolves_to[x3].evolves_to[x4].evolution_details[0].min_level
#                                except: pmMinLevel = None

#                                try: pmEvoItem = pokemonEvoChain[0].chain.evolves_to[x1].evolves_to[x2].evolves_to[x3].evolves_to[x4].evolution_details[0].item.name
#                                except: pmEvoItem = None

#                                print("From: " + pmFrom + " To: " + pmTo)
#                                print("From: " + str(pmFromDex) + " To: " + str(pmToDex))
#                                print("Min-Level: " + str(pmMinLevel))
#                                print("================================Item: " + str(pmEvoItem))

#                                parameters = (pmFromDex,pmToDex,pmMinLevel,pmEvoItem,)
#                                c.execute("INSERT INTO evolutions (evoDex, evoNextDex, evoNextItem,evoNextLevel) VALUES (?,?,?,?)",parameters)
#                                conn.commit()
#                            except: pass
#        except: pass
#except: print("Done")






for j in range(1,803):
    try: 
        #pokemon = client.get_pokemon(j)
        pokemonSpecies = client.get_pokemon_species(j)
        #pokemonEvoChain = client.get_evolution_chain(j)

        for x in range(0,100):
            try:
                if pokemonSpecies[0].flavor_text_entries[x].language.name=="en":
                     print(str(j)+ ": " + pokemonSpecies[0].flavor_text_entries[x].flavor_text)
                     parameters = (pokemonSpecies[0].flavor_text_entries[x].flavor_text,j,)
                     c.execute("UPDATE pokemon SET dexInfo = ? WHERE nationalDex = ?",parameters)
                     conn.commit()
                     print()
                     break
            except: pass
       
        
        


        
    except: pass



#conn.close()

#for j in range(1,100):
#    print("Start of " + str(j))
#    try:
#        pokemon = client.get_pokemon(j)
#        pokemonSpecies = client.get_pokemon_species(j)
#        pokemonEvoChain = client.get_evolution_chain(j)
#        pokemonGrowthRate = client.get_growth_rate(j)
    
#        # Pokedexes
#        national = None
#        kanto = None
#        original_johto = None
#        updated_johto = None
#        hoenn = None
#        updated_hoenn = None
#        original_sinnoh = None
#        extended_sinnoh = None
#        kalos_central = None
#        kalos_mountain = None
#        kalos_coastal = None
#        original_unova = None
#        updated_unova = None
#        conquest_gallery = None
        
#        try:
#            i = 0
#            while pokemonSpecies[0].pokedex_numbers[i].pokedex.name != None:
#                if str(pokemonSpecies[0].pokedex_numbers[i].pokedex.name) == "national" : national = pokemonSpecies[0].pokedex_numbers[i].entry_number
#                if str(pokemonSpecies[0].pokedex_numbers[i].pokedex.name) == "kanto" : kanto = pokemonSpecies[0].pokedex_numbers[i].entry_number
#                if str(pokemonSpecies[0].pokedex_numbers[i].pokedex.name) == "original-johto" : original_johto = pokemonSpecies[0].pokedex_numbers[i].entry_number
#                if str(pokemonSpecies[0].pokedex_numbers[i].pokedex.name) == "updated-johto" : updated_johto = pokemonSpecies[0].pokedex_numbers[i].entry_number
#                if str(pokemonSpecies[0].pokedex_numbers[i].pokedex.name) == "hoenn" : hoenn = pokemonSpecies[0].pokedex_numbers[i].entry_number
#                if str(pokemonSpecies[0].pokedex_numbers[i].pokedex.name) == "updated-hoenn" : updated_hoenn = pokemonSpecies[0].pokedex_numbers[i].entry_number
#                if str(pokemonSpecies[0].pokedex_numbers[i].pokedex.name) == "original-sinnoh" : original_sinnoh = pokemonSpecies[0].pokedex_numbers[i].entry_number
#                if str(pokemonSpecies[0].pokedex_numbers[i].pokedex.name) == "extended-sinnoh" : extended_sinnoh = pokemonSpecies[0].pokedex_numbers[i].entry_number
#                if str(pokemonSpecies[0].pokedex_numbers[i].pokedex.name) == "kalos-central" : kalos_central = pokemonSpecies[0].pokedex_numbers[i].entry_number
#                if str(pokemonSpecies[0].pokedex_numbers[i].pokedex.name) == "kalos-mountain" : kalos_mountain = pokemonSpecies[0].pokedex_numbers[i].entry_number
#                if str(pokemonSpecies[0].pokedex_numbers[i].pokedex.name) == "kalos-coastal" : kalos_coastal = pokemonSpecies[0].pokedex_numbers[i].entry_number
#                if str(pokemonSpecies[0].pokedex_numbers[i].pokedex.name) == "original-unova" : original_unova = pokemonSpecies[0].pokedex_numbers[i].entry_number
#                if str(pokemonSpecies[0].pokedex_numbers[i].pokedex.name) == "updated-unova" : updated_unova = pokemonSpecies[0].pokedex_numbers[i].entry_number
#                if str(pokemonSpecies[0].pokedex_numbers[i].pokedex.name) == "conquest-gallery" : conquest_gallery = pokemonSpecies[0].pokedex_numbers[i].entry_number
#                i += 1
#        except: pass

#        # Types
#        if pokemon[0].types[0].slot == 1:
#            type1 = pokemon[0].types[0].type.name
#            type2 = None
#        else:
#            type1 = pokemon[0].types[1].type.name
#            type2 = pokemon[0].types[0].type.name

#        if str(type1) == "bug": type1 = 1
#        elif str(type1) == "dark": type1 = 2
#        elif str(type1) == "dragon": type1 = 3
#        elif str(type1) == "electric": type1 = 4
#        elif str(type1) == "fairy": type1 = 5
#        elif str(type1) == "fighting": type1 = 6
#        elif str(type1) == "fire": type1 = 7
#        elif str(type1) == "flying": type1 = 8
#        elif str(type1) == "ghost": type1 = 9
#        elif str(type1) == "grass": type1 = 10
#        elif str(type1) == "ground": type1 = 11
#        elif str(type1) == "ice": type1 = 12
#        elif str(type1) == "normal": type1 = 13
#        elif str(type1) == "poison": type1 = 14
#        elif str(type1) == "psychic": type1 = 15
#        elif str(type1) == "rock": type1 = 16
#        elif str(type1) == "steel": type1 = 17
#        elif str(type1) == "water": type1 = 18
#        else: type1 = 0 

#        if str(type2) == "bug": type2 = 1
#        elif str(type2) == "dark": type2 = 2
#        elif str(type2) == "dragon": type2 = 3
#        elif str(type2) == "electric": type2 = 4
#        elif str(type2) == "fairy": type2 = 5
#        elif str(type2) == "fighting": type2 = 6
#        elif str(type2) == "fire": type2 = 7
#        elif str(type2) == "flying": type2 = 8
#        elif str(type2) == "ghost": type2 = 9
#        elif str(type2) == "grass": type2 = 10
#        elif str(type2) == "ground": type2 = 11
#        elif str(type2) == "ice": type2 = 12
#        elif str(type2) == "normal": type2 = 13
#        elif str(type2) == "poison": type2 = 14
#        elif str(type2) == "psychic": type2 = 15
#        elif str(type2) == "rock": type2 = 16
#        elif str(type2) == "steel": type2 = 17
#        elif str(type2) == "water": type2 = 18
#        else: type2 = 0 

#        # Generations
#        if pokemonSpecies[0].generation.name == "generation-i": generation = 1
#        elif pokemonSpecies[0].generation.name == "generation-ii": generation = 2
#        elif pokemonSpecies[0].generation.name == "generation-iii": generation = 3
#        elif pokemonSpecies[0].generation.name == "generation-iv": generation = 4
#        elif pokemonSpecies[0].generation.name == "generation-v": generation = 5
#        elif pokemonSpecies[0].generation.name == "generation-vi": generation = 6
#        elif pokemonSpecies[0].generation.name == "generation-vii": generation = 7

#        # Egg Groups
#        try:
#            i = 0
#            while pokemonSpecies[0].egg_groups[i].name != None:
#                #print(pokemonSpecies[0].egg_groups[i].name)
#                i += 1
#        except: pass

#        # Names and Description
#        nameEN = pokemonSpecies[0].names[2].name
#        nameDE = pokemonSpecies[0].names[5].name

#        dexInfo = None

#        # Order
#        order = pokemon[0].order

#        # Height and Weight
#        height = pokemon[0].height
#        weight = pokemon[0].weight

#        # Stats
#        statHP = pokemon[0].stats[5].base_stat
#        statAtk = pokemon[0].stats[4].base_stat
#        statDef = pokemon[0].stats[3].base_stat
#        statSpAtk = pokemon[0].stats[2].base_stat
#        statSpDef = pokemon[0].stats[1].base_stat
#        statSpd = pokemon[0].stats[0].base_stat

#        # Genders
#        genderMale = 100 - (100/(pokemonSpecies[0].gender_rate*8))
#        genderFemale = 100/(pokemonSpecies[0].gender_rate*8)

#        genderDifference = pokemonSpecies[0].has_gender_differences

#        # Other
#        catchRate = pokemonSpecies[0].capture_rate
#        baseFriendship = pokemonSpecies[0].base_happiness
#        baseExp = pokemon[0].base_experience
        
#        # Growth Rate
#        growthRate = pokemonSpecies[0].growth_rate.name

#       if str(growthRate) == "slow": gRate = 1
#       if str(growthRate) == "medium": gRate = 2
#       if str(growthRate) == "fast": gRate = 3
#       if str(growthRate) == "medium-slow": gRate = 4
#       if str(growthRate) == "slow-then-very-fast": gRate = 5
#       if str(growthRate) == "fast-then-very-slow": gRate = 6

#        # EggGroup
#        eggGroup = pokemonSpecies[0].egg_groups[0].name

#        if str(eggGroup) == "monster": eGr = 1
#        elif str(eggGroup) == "water1": eGr = 2
#        elif str(eggGroup) == "water2": eGr = 3
#        elif str(eggGroup) == "water3": eGr = 4
#        elif str(eggGroup) == "bug": eGr = 5
#        elif str(eggGroup) == "flying": eGr = 6
#        elif str(eggGroup) == "ground": eGr = 7
#        elif str(eggGroup) == "fairy": eGr = 8
#        elif str(eggGroup) == "plant": eGr = 9
#        elif str(eggGroup) == "humanshape": eGr = 10
#        elif str(eggGroup) == "mineral": eGr = 11
#        elif str(eggGroup) == "indeterminate": eGr = 12
#        elif str(eggGroup) == "ditto": eGr = 13
#        elif str(eggGroup) == "dragon": eGr = 14
#        elif str(eggGroup) == "no-eggs": eGr = 15
#        else: eGr = None

#        evPoints = pokemon[0].stats[0].effort
        #evType = pokemon[0].stats[0].stat.name

        #for x in range(0,6):
        #    evYieldType = pokemon[0].stats[x].stat.name

        #    if pokemon[0].stats[x].effort != 0:

        #        if evYieldType == "hp": evYieldID = 1
        #        if evYieldType == "attack": evYieldID = 2
        #        if evYieldType == "defense": evYieldID = 3
        #        if evYieldType == "special-attack": evYieldID = 4
        #        if evYieldType == "special-defense": evYieldID = 5
        #        if evYieldType == "speed": evYieldID = 6

        #        evPoints = pokemon[0].stats[x].effort

        #        print(str(j) + ": " + str(evPoints) + " " + evYieldType + " (" + str(evYieldID) + ")")
            
        #        parameters = (j,evYieldID,evPoints,)
        #        c.execute("INSERT INTO evYields (nationalDex,evYieldTypeID,evYieldPoints) VALUES (?,?,?)",parameters)
        #        conn.commit()

#        print(nameDE)

#    except: pass

##   Pokemon Species
#    print(pokemonSpecies[0].genera[2].genus)


    






## Egg Groups
#i = 0
#try:
#    while pokemonSpecies[0].egg_groups[i].name != None:
#        #print(pokemonSpecies[0].egg_groups[i].name)
#        i += 1
#except IndexError: pass


## doesn't really work...
#nextEvolutionName = pokemonEvoChain[0].chain.evolves_to[0].species.name