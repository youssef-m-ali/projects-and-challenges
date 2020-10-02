#First we import libraries we might need

from grove_library import *
from time import sleep

#Next we define functions we will call in the script

'''
assumes Arduino is connected to a properly initiated Chainable LED
prints the light sensor reading and the level on a scale from 1-4
sets the LED brightness according to the level
'''
def streetLight():
    lightSensor = arduinoAnalogRead(0)
    print (lightSensor)
    if lightSensor <= 300 and lightSensor > 200:
        chainLEDSetColour(streetLED,40,40,0)
        print('1')

    elif lightSensor < 200 and lightSensor > 100:
        chainLEDSetColour(streetLED,80,80,0)
        print('2')

    elif lightSensor < 100:
        chainLEDSetColour(streetLED,255,255,0)
        print('3')

    else:
        chainLEDSetColour(streetLED,0,0,0)
        print('4')
        
'''
assumes Arduino is connected to a properly initiated Chainable LED with at least 2 LEDs
sets the LEDs to move the traffic in the main road
'''
def mainRoadTraffic():
    global var_side
    global var_main
    if var_side == 1:
        
        sleep(2)
        chainLEDSetColour(sideCarLED,255,255,0)
        chainLEDSetColour(mainPedLED,255,0,0)
        streetLight()
        
        sleep(2)
        chainLEDSetColour(sideCarLED,255,0,0)
        streetLight()
        
        sleep(2)
        chainLEDSetColour(mainCarLED,0,255,0)
        chainLEDSetColour(sidePedLED,0,255,0)
        streetLight()
        
        sleep(2)
        var_side = 0
        var_main = 1
        streetLight()
        

'''
assumes Arduino is connected to a properly initiated Chainable LED with at least 2 LEDs
sets the LEDs to move the traffic in the side road
'''

def sideRoadTraffic():
    global var_side
    global var_main
    if var_main == 1:
        
        sleep(2)
        chainLEDSetColour(mainCarLED,255,255,0)
        chainLEDSetColour(sidePedLED,255,0,0)
        streetLight()
        
        sleep(2)
        chainLEDSetColour(mainCarLED,255,0,0)
        streetLight()
        
        sleep(2)
        chainLEDSetColour(sideCarLED,0,255,0)
        chainLEDSetColour(mainPedLED,0,255,0)
        streetLight()
        
        sleep(2)
        var_main = 0
        var_side = 1
        streetLight()

'''
assumes the Arduino is connected to a properly initiated ultrasonic sensor
returns the queue updated or not according to the ultrasonic reading
'''
    
def ultrasonic():
    ultraSensor  = ultraGetDistance()
    if ultraSensor  < 3:
        actions.append("CarS")
    return actions
        
    

'''
assumes Arduino is connected to 4 push buttons
returns the queue updated or not according to the value of the push buttons
        eliminates duplicates from the queue
'''    

def crossers():
    
    lower = arduinoDigitalRead(4)
    upper = arduinoDigitalRead(3)
    right = arduinoDigitalRead(6)
    left  = arduinoDigitalRead(5)
    
    if upper == 1 or lower == 1:
        actions.append("PS")
        
    if right == 1 or left == 1:
        actions.append("PM")
        
    actions = list(dict.fromkeys(actions))
    return actions


'''
assumes Arduino is connected to a properly initialized speaker
plays a high note on a slow pattern
'''  
def mainSpeaker ():
    
    for i in range(3):
        speakerPlayNote(350, 1)
        sleep(3)

'''
assumes Arduino is connected to a properly initialized speaker
plays a low note on a quick pattern
'''  
def sideSpeaker ():
    
    for i in range(3):
        speakerPlayNote(150, 1)
        sleep(2)
        

#Now we have the script that will run#       
    


# Call function to initialize the Arduino
connection = arduinoInit(0)

# Initialize components that require it
chainLEDInit(2, 5, connection)
ultraInit(7, connection)
speakerInit(8, connection)

#Replace literal values with index values for chainable LEDs
sidePedLED = 0
mainPedLED = 1
mainCarLED = 2
sideCarLED = 3
streetLED = 4

#Set default values
chainLEDSetColour(sidePedLED,0,255,0)
chainLEDSetColour(mainPedLED,255,0,0)
chainLEDSetColour(2,0,255,0)
chainLEDSetColour(3,255,0,0)

var_side = 0
var_main = 1

# Create empty list to form a queue
actions = []


while 1:


    
    streetLight()
    crossers()
    ultrasonic()
    
    
    while len(actions) != 0:
        
        if actions[0] == "PM" :
            
            sideRoadTraffic()
            mainSpeaker()
            
            crossers()
            streetLight()
            
            actions.remove("PM")
          
        elif actions[0] == "PS" :
            
            mainRoadTraffic()
            sideSpeaker()
            
            crossers()
            streetLight()
            
            actions.remove ("PS")
           
        elif actions[0] == "CarS":
            
            while "CarS" in actions:
                sideRoadTraffic()
                mainSpeaker()
                
                ultrasonic()
                crossers()
                streetLight()
                
                actions.remove ("CarS")

    if len(actions) == 0:
        
            mainRoadTraffic()
            sideSpeaker()
