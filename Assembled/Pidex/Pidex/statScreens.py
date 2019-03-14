class StatScreen:

    

    def Load(pageNumber,surface,pokeData,color, attr = None):

        if pageNumber == 0: StatScreen.StatSet0(surface,pokeData,color)
        elif pageNumber == 1: StatScreen.StatSet1(surface,pokeData,color)
        elif pageNumber == 2: StatScreen.StatSet2(surface,pokeData,color,attr[0])
        elif pageNumber == 3: StatScreen.StatSet3(surface,pokeData,color)
        elif pageNumber == 4: StatScreen.StatSet4(surface,pokeData,color)
        elif pageNumber == 5: StatScreen.StatSet5(surface,pokeData,color,attr[1],attr[2],attr[3],attr[4])

    def StatSet0(surface,pokeData,color):

        import pygame
        from basics import Basic

        Basic.WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",color,False)     
        Basic.WriteText(surface,(40,35),pokeData["regionName"],30,"PokemonHollow.ttf",color,False)     
        Basic.WriteText(surface,(260,45),"#" + str('{0:03d}'.format(pokeData["nationalDex"])),50,"PokemonHollow.ttf",color,True)     

        Basic.WriteText(surface,(150,100),"Pokédex Data",30,"PokemonSolid.ttf",color,True)  
    
        Basic.WriteText(surface,(30,145),"National Dex:",20,"calibrilight.ttf",color,False)    
        Basic.WriteText(surface,(150,145),"#" + str('{0:03d}'.format(pokeData["nationalDex"])),25,"calibrilight.ttf",color,False)    

        Basic.WriteText(surface,(30,170),str(pokeData["regionName"]) + " Dex:",20,"calibrilight.ttf",color,False)    
        Basic.WriteText(surface,(150,170),"#" + str('{0:03d}'.format(pokeData["nationalDex"])),25,"calibrilight.ttf",color,False)    

        Basic.WriteText(surface,(30,220),"Species:",20,"calibrilight.ttf",color,False)    
        Basic.WriteText(surface,(110,220),pokeData["species"],25,"calibrilight.ttf",color,False)    

        Basic.WriteText(surface,(30,290),"Type:",20,"calibrilight.ttf",color,False) 

        if pokeData["type2NameEN"] == None:
            Basic.WriteText(surface,(150,275),pokeData["type1NameEN"],20,"calibrilight.ttf",color,True)
            surface.blit(pygame.image.load("typesS/" + pokeData["type1IconImage"]),(150-25,285))
        else:
            Basic.WriteText(surface,(150,275),pokeData["type1NameEN"] + " / " + pokeData["type2NameEN"],20,"calibrilight.ttf",color,True)
            surface.blit(pygame.image.load("typesS/"+ pokeData["type1IconImage"]),(150-25-30,285))
            surface.blit(pygame.image.load("typesS/"+ pokeData["type2IconImage"]),(150-25+30,285))

        Basic.WriteText(surface,(30,360),"Height:",20,"calibrilight.ttf",color,False)    
        Basic.WriteText(surface,(100,360),str(pokeData["height"]/10) + "m",25,"calibrilight.ttf",color,False)  

        Basic.WriteText(surface,(30,390),"Weight:",20,"calibrilight.ttf",color,False)    
        Basic.WriteText(surface,(100,390),str(pokeData["weight"]/10) + "kg",25,"calibrilight.ttf",color,False)  

    def StatSet1(surface,pokeData,color):

        import pygame
        from basics import Basic

        Basic.WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",color,False)     
        Basic.WriteText(surface,(40,35),pokeData["regionName"],30,"PokemonHollow.ttf",color,False)     
        Basic.WriteText(surface,(260,45),"#" + str('{0:03d}'.format(pokeData["nationalDex"])),50,"PokemonHollow.ttf",color,True)    

        Basic.WriteText(surface,(150,100),"Pokédex entry",30,"PokemonSolid.ttf",color,True) 

        Basic.BlitText(surface, str(pokeData["dexInfo"]), (20, 130),pygame.font.Font("calibrilight.ttf",20),(255,255,255))

    def StatSet2(surface,pokeData,color,barColor):

        from basics import Basic

        Basic.WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",color,False)     
        Basic.WriteText(surface,(40,35),pokeData["regionName"],30,"PokemonHollow.ttf",color,False)     
        Basic.WriteText(surface,(260,45),"#" + str('{0:03d}'.format(pokeData["nationalDex"])),50,"PokemonHollow.ttf",color,True)     

        Basic.WriteText(surface,(150,100),"Base Stats",30,"PokemonSolid.ttf",color,True)    

        Basic.ProgressBar(surface,(50,160),200,18,barColor,"HP",0,150,pokeData["statHP"])
        Basic.ProgressBar(surface,(50,210),200,18,barColor,"Attack",0,150,pokeData["statAtk"])
        Basic.ProgressBar(surface,(50,260),200,18,barColor,"Defense",0,150,pokeData["statDef"])
        Basic.ProgressBar(surface,(50,310),200,18,barColor,"Sp. Atk",0,150,pokeData["statSpAtk"])
        Basic.ProgressBar(surface,(50,360),200,18,barColor,"Sp. Def",0,150,pokeData["statSpDef"])
        Basic.ProgressBar(surface,(50,410),200,18,barColor,"Speed",0,150,pokeData["statSpd"])

    def StatSet3(surface,pokeData,color):

        from basics import Basic

        Basic.WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",color,False)     
        Basic.WriteText(surface,(40,35),pokeData["regionName"],30,"PokemonHollow.ttf",color,False)     
        Basic.WriteText(surface,(260,45),"#" + str('{0:03d}'.format(pokeData["nationalDex"])),50,"PokemonHollow.ttf",color,True)    

        Basic.WriteText(surface,(150,100),"Training",30,"PokemonSolid.ttf",color,True)    

        Basic.WriteText(surface,(30,145),"EV Yield:",20,"calibrilight.ttf",color,False)    
        Basic.WriteText(surface,(170,145),str(pokeData["evYieldAmt"]) + " " +  str(pokeData["evYieldTypeEN"]),25,"calibrilight.ttf",color,False)    

        Basic.WriteText(surface,(30,185),"Catch Rate:",20,"calibrilight.ttf",color,False)    
        Basic.WriteText(surface,(170,185),str(pokeData["catchRate"]) + "%",25,"calibrilight.ttf",color,False)    

        Basic.WriteText(surface,(30,225),"Base Friendship:",20,"calibrilight.ttf",color,False)    
        Basic.WriteText(surface,(170,225),str(pokeData["baseFriendship"]),25,"calibrilight.ttf",color,False)    

        Basic.WriteText(surface,(30,265),"Base Exp.:",20,"calibrilight.ttf",color,False)    
        Basic.WriteText(surface,(170,265),str(pokeData["baseExp"]),25,"calibrilight.ttf",color,False)  

        Basic.WriteText(surface,(30,305),"Growth Rate:",20,"calibrilight.ttf",color,False)    
        Basic.WriteText(surface,(170,305),str(pokeData["growthRateEN"]),25,"calibrilight.ttf",color,False)  

    def StatSet4(surface,pokeData,color):

        from basics import Basic

        Basic.WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",color,False)     
        Basic.WriteText(surface,(40,35),pokeData["regionName"],30,"PokemonHollow.ttf",color,False)     
        Basic.WriteText(surface,(260,45),"#" + str('{0:03d}'.format(pokeData["nationalDex"])),50,"PokemonHollow.ttf",color,True)    

        Basic.WriteText(surface,(150,100),"Breeding",30,"PokemonSolid.ttf",color,True)    

        Basic.WriteText(surface,(30,145),"Egg Groups:",20,"calibrilight.ttf",color,False)    
        Basic.WriteText(surface,(170,145),pokeData["eggGroupNameEN"],25,"calibrilight.ttf",color,False)    

        Basic.WriteText(surface,(30,185),"Gender:",20,"calibrilight.ttf",color,False)    
        Basic.WriteText(surface,(170,185),str(pokeData["genderMale"]) + "% male",25,"calibrilight.ttf",color,False)    
        Basic.WriteText(surface,(170,220),str(100-pokeData["genderMale"]) + "% female",25,"calibrilight.ttf",color,False)    

        Basic.WriteText(surface,(30,260),"Egg cycles:",20,"calibrilight.ttf",color,False)    
        Basic.WriteText(surface,(170,260),str(pokeData["eggCycles"]),25,"calibrilight.ttf",color,False)  

    def StatSet5(surface,pokeData,color,genderDifference,buttonColor,textColor,action):

        from basics import Basic

        Basic.WriteText(surface,(40,5),"Region:",20,"PokemonSolid.ttf",color,False)     
        Basic.WriteText(surface,(40,35),pokeData["regionName"],30,"PokemonHollow.ttf",color,False)     
        Basic.WriteText(surface,(260,45),"#" + str('{0:03d}'.format(pokeData["nationalDex"])),50,"PokemonHollow.ttf",color,True)   

        Basic.WriteText(surface,(150,100),"Appearance",30,"PokemonSolid.ttf",color,True)    


        # Gender / Shiny Button and update

        if genderDifference:
            Basic.WriteText(surface,(165,150),"Male:",25,"calibrilight.ttf",color,True) 
            Basic.Button(surface,(100,180),20,"Normal",20,buttonColor,textColor,action,"FNM",(470,0))
            Basic.Button(surface,(230,180),20,"Shiny",20,buttonColor,textColor,action,"FSM",(470,0))

            Basic.WriteText(surface,(165,220),"Female:",25,"calibrilight.ttf",color,True) 
            Basic.Button(surface,(100,250),20,"Normal",20,buttonColor,textColor,action,"FNF",(470,0))
            Basic.Button(surface,(230,250),20,"Shiny",20,buttonColor,textColor,action,"FSF",(470,0))

            Basic.WriteText(surface,(165,300),"Backside:",25,"calibrilight.ttf",color,True) 
            Basic.Button(surface,(100,330),20,"Normal",20,buttonColor,textColor,action,"BN",(470,0))
            Basic.Button(surface,(230,330),20,"Shiny",20,buttonColor,textColor,action,"BS",(470,0))
        else:
            Basic.WriteText(surface,(165,150),"Frontside:",25,"calibrilight.ttf",color,True) 
            Basic.Button(surface,(100,180),20,"Normal",20,buttonColor,textColor,action,"FN",(470,0))
            Basic.Button(surface,(230,180),20,"Shiny",20,buttonColor,textColor,action,"FS",(470,0))

            Basic.WriteText(surface,(165,220),"Backside:",25,"calibrilight.ttf",color,True) 
            Basic.Button(surface,(100,250),20,"Normal",20,buttonColor,textColor,action,"BN",(470,0))
            Basic.Button(surface,(230,250),20,"Shiny",20,buttonColor,textColor,action,"BS",(470,0))

        Basic.WriteText(surface,(165,380),"Attack Animation:",25,"calibrilight.ttf",color,True) 
        Basic.Button(surface,(165,410),20,"Toggle",20,buttonColor,textColor,action,"ATK",(470,0))
