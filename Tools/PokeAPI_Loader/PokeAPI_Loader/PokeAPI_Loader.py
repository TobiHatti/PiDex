import pokepy


client = pokepy.V2Client()

running = True
selectedDex = 0

while running:
    selectedDex = int(input("=============================\n\nEnter DEX-Number: "))
    

    print("\nData for Dex #" + str(selectedDex) + ":\n")

    try: pokemon = client.get_pokemon(selectedDex)
    except: print("Error 001: Could not load Data \"Pokemon\"")

    try: pokemonSpecies = client.get_pokemon_species(selectedDex)
    except: print("Error 002: Could not load Data \"PokemonSpecies\"")




    try: pokemonShape = client.get_pokemon_shape(selectedDex)
    except: print("Error 005: Could not load Data \"PokemonShape\"")

    

    print("")

    print("Name [EN]: \t" + pokemonSpecies[0].names[2].name)
    print("Name [DE]: \t" + pokemonSpecies[0].names[5].name)


    if pokemon[0].types[0].slot == 1: print("Type: " + pokemon[0].types[0].type.name)
    else: print("Types: \t\t" + pokemon[0].types[1].type.name + ", " + pokemon[0].types[0].type.name)

    print("Generation:\t" + pokemonSpecies[0].generation.name)
    print("Height: \t" + str(pokemon[0].height/10) + "m")
    print("Weight: \t" + str(pokemon[0].weight/10) + "kg")

    print("HP:\t\t" + str(pokemon[0].stats[5].base_stat))
    print("Attack:\t\t" + str(pokemon[0].stats[4].base_stat))
    print("Defense:\t" + str(pokemon[0].stats[3].base_stat))
    print("Special Atk:\t" + str(pokemon[0].stats[2].base_stat))
    print("Special Def:\t" + str(pokemon[0].stats[1].base_stat))
    print("Speed:\t\t" + str(pokemon[0].stats[0].base_stat))

    print("Genderrate M:\t" + str(100 - (100/(pokemonSpecies[0].gender_rate*8))) + "%")
    print("Genderrate F:\t" + str(100/(pokemonSpecies[0].gender_rate*8)) + "%")

    try:
        i = 0
        while pokemonSpecies[0].egg_groups[i].name != None:
            print("Egg-Group:\t" + pokemonSpecies[0].egg_groups[0].name)
            i += 1
    except: pass

    print("Growth-Rate:\t" + pokemonSpecies[0].growth_rate.name)

    print("Effort Points:\t" + str(pokemon[0].stats[0].effort))
    print("Effort Type:\t" + pokemon[0].stats[0].stat.name)
    print("EV-Yield:\t" + str(pokemon[0].stats[0].effort) + " " + pokemon[0].stats[0].stat.name)

    print("Catch Rate:\t" + str(pokemonSpecies[0].capture_rate))
    print("Base Friendship:" + str(pokemonSpecies[0].base_happiness))
    print("Base Exp:\t" + str(pokemon[0].base_experience))
    print("Egg cycles:\t" + str(pokemonSpecies[0].hatch_counter))
    
