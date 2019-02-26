import sqlite3
import pokepy
import urllib.request
import os


client = pokepy.V2Client()


#for j in range(1,803):
#    try:
#        pokemon = client.get_pokemon(j)
        
#        #print(pokemon[0].sprites.back_female)
#        #print(pokemon[0].sprites.back_shiny_female)
#        #print(pokemon[0].sprites.back_default)
#        #print(pokemon[0].sprites.front_female)
#        #print(pokemon[0].sprites.front_shiny_female)
#        #print(pokemon[0].sprites.back_shiny)
#        #print(pokemon[0].sprites.front_default)
#        print(pokemon[0].sprites.front_shiny)

#        urllib.request.urlretrieve(pokemon[0].sprites.front_shiny, "sprites/" + str('{0:03d}'.format(j)) + "/sprite-small-FS-" + str('{0:03d}'.format(j)) + ".png")
#    except: print("Could not load " + str(j))
 
for j in range(1,803):
    try:
        pokemon = client.get_pokemon(j)
        
        #print(pokemon[0].sprites.back_female)
        #print(pokemon[0].sprites.back_shiny_female)
        #print(pokemon[0].sprites.back_default)
        #print(pokemon[0].sprites.front_female)
        #print(pokemon[0].sprites.front_shiny_female)
        #print(pokemon[0].sprites.back_shiny)
        print(pokemon[0].sprites.front_default)
        #print(pokemon[0].sprites.front_shiny)

        urllib.request.urlretrieve(pokemon[0].sprites.front_default, "sprites/" + str('{0:03d}'.format(j)) + "/sprite-small-FN-" + str('{0:03d}'.format(j)) + ".png")
    except: print("Could not load " + str(j))
 
for j in range(1,803):
    try:
        pokemon = client.get_pokemon(j)
        
        #print(pokemon[0].sprites.back_female)
        #print(pokemon[0].sprites.back_shiny_female)
        #print(pokemon[0].sprites.back_default)
        #print(pokemon[0].sprites.front_female)
        #print(pokemon[0].sprites.front_shiny_female)
        print(pokemon[0].sprites.back_shiny)
        #print(pokemon[0].sprites.front_default)
        #print(pokemon[0].sprites.front_shiny)

        urllib.request.urlretrieve(pokemon[0].sprites.back_shiny, "sprites/" + str('{0:03d}'.format(j)) + "/sprite-small-BS-" + str('{0:03d}'.format(j)) + ".png")
    except: print("Could not load " + str(j))

for j in range(1,803):
    try:
        pokemon = client.get_pokemon(j)
        
        #print(pokemon[0].sprites.back_female)
        #print(pokemon[0].sprites.back_shiny_female)
        #print(pokemon[0].sprites.back_default)
        #print(pokemon[0].sprites.front_female)
        print(pokemon[0].sprites.front_shiny_female)
        #print(pokemon[0].sprites.back_shiny)
        #print(pokemon[0].sprites.front_default)
        #print(pokemon[0].sprites.front_shiny)

        urllib.request.urlretrieve(pokemon[0].sprites.front_shiny_female, "sprites/" + str('{0:03d}'.format(j)) + "/sprite-small-FSF-" + str('{0:03d}'.format(j)) + ".png")
    except: print("Could not load " + str(j))

for j in range(1,803):
    try:
        pokemon = client.get_pokemon(j)
        
        #print(pokemon[0].sprites.back_female)
        #print(pokemon[0].sprites.back_shiny_female)
        #print(pokemon[0].sprites.back_default)
        print(pokemon[0].sprites.front_female)
        #print(pokemon[0].sprites.front_shiny_female)
        #print(pokemon[0].sprites.back_shiny)
        #print(pokemon[0].sprites.front_default)
        #print(pokemon[0].sprites.front_shiny)

        urllib.request.urlretrieve(pokemon[0].sprites.front_female, "sprites/" + str('{0:03d}'.format(j)) + "/sprite-small-FNF-" + str('{0:03d}'.format(j)) + ".png")
    except: print("Could not load " + str(j))

for j in range(1,803):
    try:
        pokemon = client.get_pokemon(j)
        
        #print(pokemon[0].sprites.back_female)
        #print(pokemon[0].sprites.back_shiny_female)
        print(pokemon[0].sprites.back_default)
        #print(pokemon[0].sprites.front_female)
        #print(pokemon[0].sprites.front_shiny_female)
        #print(pokemon[0].sprites.back_shiny)
        #print(pokemon[0].sprites.front_default)
        #print(pokemon[0].sprites.front_shiny)

        urllib.request.urlretrieve(pokemon[0].sprites.back_default, "sprites/" + str('{0:03d}'.format(j)) + "/sprite-small-BN-" + str('{0:03d}'.format(j)) + ".png")
    except: print("Could not load " + str(j))

for j in range(1,803):
    try:
        pokemon = client.get_pokemon(j)
        
        #print(pokemon[0].sprites.back_female)
        print(pokemon[0].sprites.back_shiny_female)
        #print(pokemon[0].sprites.back_default)
        #print(pokemon[0].sprites.front_female)
        #print(pokemon[0].sprites.front_shiny_female)
        #print(pokemon[0].sprites.back_shiny)
        #print(pokemon[0].sprites.front_default)
        #print(pokemon[0].sprites.front_shiny)

        urllib.request.urlretrieve(pokemon[0].sprites.back_shiny_female, "sprites/" + str('{0:03d}'.format(j)) + "/sprite-small-BSF-" + str('{0:03d}'.format(j)) + ".png")
    except: print("Could not load " + str(j))

for j in range(1,803):
    try:
        pokemon = client.get_pokemon(j)
        
        print(pokemon[0].sprites.back_female)
        #print(pokemon[0].sprites.back_shiny_female)
        #print(pokemon[0].sprites.back_default)
        #print(pokemon[0].sprites.front_female)
        #print(pokemon[0].sprites.front_shiny_female)
        #print(pokemon[0].sprites.back_shiny)
        #print(pokemon[0].sprites.front_default)
        #print(pokemon[0].sprites.front_shiny)

        urllib.request.urlretrieve(pokemon[0].sprites.back_female, "sprites/" + str('{0:03d}'.format(j)) + "/sprite-small-BNF-" + str('{0:03d}'.format(j)) + ".png")
    except: print("Could not load " + str(j))