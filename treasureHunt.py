# This is the minecraft library
import mcpi.minecraft as minecraft
import math
import random
import time
import RPi.GPIO as GPIO

#  Control 3 LEDs connected to pins 18, 23 and 24 on the PI
def ledControl(led, status):

    # First decide which LED to control
    if led == "R":
        ledNumber = 18
    elif led == "A":
        ledNumber = 23
    else:
        ledNumber = 24
        
    # Now, turn it on or off depending on the status
    if status == 1:
        GPIO.output(ledNumber,GPIO.HIGH)
    else:
        GPIO.output(ledNumber,GPIO.LOW)        

# Set up the GPIO pins
def GPIOSetUp():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(18,GPIO.OUT)
    GPIO.setup(23,GPIO.OUT)
    GPIO.setup(24,GPIO.OUT)

# Tidy up GPIO
def GPIOShutDown():
    GPIO.cleanup()


# Find the distance between 2 points in 3D space, uses pythagoras
def distanceBetweenItems(x1, y1, z1, x2, y2, z2):
    return math.sqrt(((x2-x1) * (x2-x1)) + ((y2-y1) * (y2-y1)) + ((z2-z1) * (z2-z1)))


# Generate a random coordinate for a minecraft world
def randomCoord():
    return(int((random.random() * 200) - 100))

# Place the treasure at the specified coordinates, just make a
# 3*3*3 block of diamond (57)
def buildTheTreasure(m,x,y,z):
    m.setBlocks(x-1, y-1, z-1, x+1, y+1, z+1, 46)

# Delete the trasure at the specified coordinates, just make a
# 3*3*3 block of air (0)
def removeTheTreasure(m,x,y,z):
    m.setBlocks(x-1, y-1, z-1, x+1, y+1, z+1, 0)



GPIOSetUp()

# Create a minecraft object
mc = minecraft.Minecraft.create()

# Pick some random coordinates for the treasure
Treasurex = randomCoord()
Treasurey = 50
Treasurez = randomCoord()

# Place the treasure
buildTheTreasure(mc,Treasurex,Treasurey,Treasurez)

print (Treasurex)
print (Treasurey)
print (Treasurez)

# Start by working out how far away we are when the program starts
# ... so we alson need to know where we are
pos = mc.player.getTilePos()
distanceToTreasure = distanceBetweenItems(pos.x, pos.y, pos.z, Treasurex, Treasurey, Treasurez)

mc.postToChat("Find the diamond blocks!")

# Start to loop until we're close to the treasure
while (distanceToTreasure) > 2:
    
    # use the post to chat function to display how far away we are
    #mc.postToChat(int(distanceToTreasure))
    print ("Distance to treasure is " + str(int(distanceToTreasure)))

    if distanceToTreasure > 75:
        ledControl("R",1)
        ledControl("A",0)
        ledControl("G",0)
    elif distanceToTreasure > 25 and distanceToTreasure <= 75:
        ledControl("R",0)
        ledControl("A",1)
        ledControl("G",0)
    else:
        ledControl("R",0)
        ledControl("A",0)
        ledControl("G",1)        

    # Wait for a second
    time.sleep(0.1)

    # Now check where I am and recalculate the distance
    pos = mc.player.getTilePos()
    # Work out the new distance to the treasure
    distanceToTreasure = distanceBetweenItems(pos.x, pos.y, pos.z, Treasurex, Treasurey, Treasurez)

    # If the treasure is above air, then move it down 1 block
    if mc.getBlock(Treasurex, Treasurey-2, Treasurez) == 0:
        removeTheTreasure(mc,Treasurex,Treasurey,Treasurez)
        Treasurey = Treasurey - 1
        buildTheTreasure(mc,Treasurex,Treasurey,Treasurez)



# Tell us we're done
mc.postToChat("You found it, well done!")

GPIOShutDown()
