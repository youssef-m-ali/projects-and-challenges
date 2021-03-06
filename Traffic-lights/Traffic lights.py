from grove_library import *
from time import sleep
import threading


class ChainableLED:
   
    def __init__(self, pin):
        self.pin = pin
    
    def red(self):
        chainLEDSetColour(self.pin, 255, 0, 0)

    def green(self):
        chainLEDSetColour(self.pin, 0, 255, 0)

    def yellow(self):
        chainLEDSetColour(self.pin, 255, 255, 0)


class Traffic:
    def __init__(self):
        
        # Call function to initialize the Arduino
        connection = arduinoInit(0)

        # Initialize components that require it
        chainLEDInit(2, 5, connection)
        ultraInit(7, connection)
        speakerInit(8, connection)

        self.sidePedestriansLED = ChainableLED(0)
        self.mainPedestriansLED = ChainableLED(1)
        self.mainCarLED = ChainableLED(2)
        self.sideCarLED = ChainableLED(3)

        #Set default values
        self.sidePedestriansLED.green()
        self.mainPedestriansLED.red()

        self.mainCarLED.green()
        self.sideCarLED.red()

        self.mainTrafficOn = 1

        # Create empty list to form a queue
        self.queue = []


    '''
    assumes Arduino is connected to a properly initiated Chainable LED with at least 2 LEDs
    sets the LEDs to move the traffic in the main road
    '''
    def mainRoadTraffic(self):

        if self.mainTrafficOn == 0:
            
            sleep(2)
            self.sideCarLED.yellow()
            self.mainPedestriansLED.red()
            
            sleep(2)
            self.sideCarLED.red()
            
            sleep(2)
            self.mainCarLED.green()
            self.sidePedestriansLED.green()
            
            sleep(2)
            self.mainTrafficOn = 1
            

    '''
    assumes Arduino is connected to a properly initiated Chainable LED with at least 2 LEDs
    sets the LEDs to move the traffic in the side road
    '''
    def sideRoadTraffic(self):

        if self.mainTrafficOn == 1:
            
            sleep(2)
            self.mainCarLED.yellow()
            self.sidePedestriansLED.red()
            
            sleep(2)
            self.mainCarLED.red()
            
            sleep(2)
            self.sideCarLED.green()
            self.mainPedestriansLED.green()
        
            self.mainTrafficOn = 0

    '''
    assumes the Arduino is connected to a properly initiated ultrasonic sensor
    returns the queue updated or not according to the ultrasonic reading
    '''
    def ultrasonic(self):

        ultraSensor  = ultraGetDistance()
        if ultraSensor  < 3:
            self.queue.append("3 side car")
        return self.queue
            
        

    '''
    assumes Arduino is connected to 4 push buttons
    updates the queue or not according to the value of the push buttons
        eliminates duplicates from the queue
    '''    
    def crossers(self):
        
        lower = arduinoDigitalRead(4)
        upper = arduinoDigitalRead(3)
        right = arduinoDigitalRead(6)
        left  = arduinoDigitalRead(5)
        
        while 1:
            if upper == 1 or lower == 1:
                self.queue.append("2 side pedestrian")
                
            if right == 1 or left == 1:
                self.queue.append("1 main pedestrian")
                
            self.queue = list(dict.fromkeys(self.queue))

            sleep(1)


    '''
    assumes Arduino is connected to a properly initialized speaker
    plays a high note on a quick pattern
    '''  
    def mainSpeaker(self):
        
        for _ in range(3):
            speakerPlayNote(350, 1)
            sleep(2)

    '''
    assumes Arduino is connected to a properly initialized speaker
    plays a low note on a slow pattern
    '''  
    def sideSpeaker(self):
        
        for _ in range(3):
            speakerPlayNote(150, 1)
            sleep(3)
            

    def loop(self):
        while 1:
            
            self.ultrasonic()
            
            while len(self.queue) != 0:
                
                if self.queue[0] == "1 main pedestrian" :
                    
                    self.sideRoadTraffic()
                    self.mainSpeaker()
                    self.queue.remove("1 main pedestrian")
                
                elif self.queue[0] == "2 side pedestrian" :
                    self.mainRoadTraffic()
                    self.queue.remove("2 side pedestrian")
                
                elif self.queue[0] == "3 side car":
                    
                    while "3 side car" in self.queue:
                        self.sideRoadTraffic()
                        self.mainSpeaker()
                        
                        self.queue.remove("3 side car")
                        self.ultrasonic()

            self.mainRoadTraffic()
            self.sideSpeaker()
    
    def run(self):
        t1 = threading.Thread(target=self.loop)
        t2 = threading.Thread(target=self.crossers)
        t1.start()
        t2.start()

if __name__ == "__main__":
    T = Traffic()
    T.run()


