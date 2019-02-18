from pygame_functions import *


screenSize(800,480)
setBackgroundColour("pink")
testSprite  = makeSprite("lucarioSpritesheet.png", 59)  # links.gif contains 32 separate frames of animation.

moveSprite(testSprite,300,300,True)
showSprite(testSprite)

nextFrame = clock()
frame = 0
while True:
    if clock() > nextFrame:                         # We only animate our character every 80ms.
        frame = (frame+1)%59                         # There are 8 frames of animation in each direction
        nextFrame += 20                             # so the modulus 8 allows it to loop

    changeSpriteImage(testSprite,frame)  # the static facing front look

    tick(120)

endWait()