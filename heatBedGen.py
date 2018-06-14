#!/usr/bin/python3


import math
import constants

class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def setX(self, x):
        self.__x = x

    def setY(self, y):
        self.__y = y



        

class Element:
    """ Constructor. Point is a list of 2 arguments [x,y]"""
    def __init__ (self, name, point1, point2):
        self.__name =  name
        self.__p1 = point1
        self.__p2 = point2
        

    #--------------------Getters and Setters---------------------------
    """ Get the element name """
    def getName (self):
        return self.__name
  
    """ Get the first point of the element"""
    def getP1(self):
        return self.__p1
  
    """ Get the second point of the element"""
    def getP2(self):
        return self.__p2

    """ set the element name """
    def setName (self, name):
        self.__name =  name
  
    """ Set the first point of the element"""
    def setP1(self, p1):
        self.__p1 = p1
  
    """ Set the second point of the element"""
    def setP2(self, p2):
        self.__p2 = p2
    
    

class Board(Element):
    
    def __init__(self, name, center_point, width, height, thickness):

        
        #initialize the constructor of the superclass
        super().__init__(name, center_point, center_point)

        
        if width < 0 :
            raise ValueError ("Width should be greather or equal to 0")
        self._width  =  width

        if height < 0 :
            raise ValueError ("Height should be grather or equal to 0")
        self._height =  height
        
        #set the copper layer thickness
        if thickness <= 0 :
            raise ValueError ("Thickness should be greather than 0")
        self._thickness = thickness



class HeatBed (Board):

    #---------------Instance variables----------------------------      
    #pad diameter
    __p_dia = 0

    #border of the board
    __border = 0

    # l/w_t constant
    __betha = 0

    #--------------------------------------------------------------
    """ Constructor """
    def __init__(self, name, center_point, width, height, trck_width, clearance, power, voltage, thickness, p_dia):

        #Calls the superclass constructor
        super().__init__(name, center_point, width, height,thickness)

        if power <= 0 :
            raise ValueError ("Power <= 0")
    
        #set the electrical power of the board in watts
        self.__power = power

        #set the betha constant
        self.__betha = thickness*math.pow(voltage,2)/(power*constants.CU_RES)

        #set the operating voltage of the board, in volts
        self.__voltage = voltage

        #set the pin pad diameter
        if p_dia > constants.DRILL:
            self.__p_dia = p_dia
        else:
            print ("Pin pad diameter should be greather than " + str (constants.DRILL) + " mm")
            print ("Switching to defalt diameter (See PDIA in constants.py)")
            self.__p_dia = constants.PDIA

        #set the track width of the board
        self.__trck_width = trck_width

        #set the clearance
        if clearance <= 0 :
            raise ValueError("Clearance <= 0")
        else:
            self.__clearance = clearance

#-------------------Getters and setters-----------------------------

    """ Set a border for the board """
    def setBorder (self, border):
        self.__border = border

        
    def getTrckWidth(self):
        return self.__trck_width

    """ Return the clearance"""
    def getClearance (self):
        return self.__clearance

#----------------------------Other methods----------------------------------------

    """ Get the height without borders"""
    def __getHwb(self):
        return self._height - 2*self.__border

    """ Get the width without borders"""
    def __getWwb(self):
        return self._width - 2*self.__border
        
    """Return the number of parallel tracks """
    def __getNmbrOfTracks (self):
        h = self.__getHwb()
        w = self.__getWwb()
        return ((2*self.__betha*self.__trck_width - math.pi*w)/2*h)

    """ Method to get the track width (the equation is m*w^2 -o*w - n = 0 """
    def __getLineSep (self):
        w = self.__getWwb()
        n = self.__getNmbrOfTracks()
        return (w/(n -1))


        
    def traceFootprint(self):
        #pin counter
        p = 1
        
        #the radius and the number of parallel tracks
        w = self.__getLineSep()
        r = w/2
        n = self.__getNmbrOfTracks()
        
        text = 'Element["" "" "" "" 0 0 0 0 0 100 ""]\n(\n'

        lines  = ""
        arcs = ""
        side = 1 #up, 0 = down
        
        #create the vertical lines and the arcs
        j = 0;
        pos = Point(0,0)
        for i in range (1, math.ceil (n)):

            #x position of the points of the line
            v_x =(i - 1)*w

            #the two y position of the two points of the line
            v_y1 = self.__p_dia
            v_y2 = v_y1 + self.__betha*w

            center1 = Point (v_x, v_y1)
            center2 = Point (v_x, v_y2)

           

            if (i -1)%2 == 0:
                j += 1
                c1_x = w*(4*j -1)/2
                c2_x = w*(4*j -3)/2
                
                pos.setX (c1_x)
                pos.setY (v_y1)
                
                arcs += Arc (pos, r, 0, -180).traceFootprint()
                
                pos.setX (c2_x)
                pos.setY (v_y2)
                arcs += Arc (pos, r, 0, 180).traceFootprint()
            

                

            v = Line (center1,center2, self.__clearance,self)

            lines += v.traceFootprint()
            

        #contatenate the string
        text += lines + arcs +"\n)\n"
        print (text)


class Pin (Element):

    """ Constructor """
    def __init__ (self, name, identifier, center_point, d, drill, clearance,  heatbed):

        #Initialize the constructor of the superclass
        super().__init__(name, center_point, center_point)

        #the diameter of the copper pad (converted from mm to 1/100 mills)
        self.__d = d/constants.MILL_PC

        #the drill diameter (converted from mm to 1/100 mills)
        self.__drill = drill/constants.MILL_PC

        #the clearance of the pin pad (converted from mm to 1/100 mills)    
        self.__clearance = clearance/constants.MILL_PC

        #the pin number
        self.__identifier = identifier

    """ Get the clearance """
    def getClearance(self):
        return self.__clearance

    """ Return the string representation of the PCB
    code for the pin"""
    def traceFootprint (self):
        pcb_str = ("\tPin ["+str(math.ceil(self.getP1().getX()/constants.MILL_PC)) + " "
                   + str(math.ceil(self.getP1().getY()/constants.MILL_PC)) + " "
                   + str(math.ceil(self.__d)) + " "+ str(math.ceil(self.__clearance)) + " "
                   + str(math.ceil(self.__clearance/4 + self.__d)) + " "
                   + str(math.ceil(self.__drill)) + " " + '"'+self.getName()+ '" "'+str(self.__identifier) + '"' + ' "round" ]\n')
        return pcb_str


class Line (Element):
    def __init__ (self,  begin_point, end_point, clearance, heatbed):
        
        #Initialize the constructor of the superclass
        super().__init__("", begin_point, end_point)

        #the clearance of the line (converted from mm to 1/100 mills)    
        self.__clearance = clearance/constants.MILL_PC

        
    def traceFootprint (self):
        pcb_str = ("\tElementLine [" + str (math.ceil (self.getP1().getX()/constants.MILL_PC)) + " "
                   + str(math.ceil(self.getP1().getY()/constants.MILL_PC)) + " "
                   + str(math.ceil(self.getP2().getX()/constants.MILL_PC)) + " "
                   + str(math.ceil(self.getP2().getY()/constants.MILL_PC)) + " "
                   + str(math.ceil(heatbed.getTrckWidth()/constants.MILL_PC)) 
                   + " ]\n")
        return pcb_str

class Arc (Element):
    
    def __init__ (self, center_point, radius, start_angle, delta_angle):
        
        #Initialize the constructor of the superclass
        super().__init__("", center_point, center_point)

        #the clearance of the line (converted from mm to 1/100 mills)    
        self.__delta_angle = delta_angle
        self.__start_angle = start_angle
        self.__radius = radius

        
    def traceFootprint (self):
        pcb_str = ("\tElementArc [" + str (math.ceil (self.getP1().getX()/constants.MILL_PC)) + " "
                   + str(math.ceil(self.getP1().getY()/constants.MILL_PC)) + " "
                   + str(math.ceil(self.__radius/constants.MILL_PC)) + " " 
                   + str(math.ceil(self.__radius/constants.MILL_PC)) + " "
                   + str(self.__start_angle) + " "
                   + str(self.__delta_angle) + " "
                   + str(math.ceil(heatbed.getTrckWidth()/constants.MILL_PC)) 
                   + " ]\n")
        return pcb_str
        

origin = Point (0,0)
heatbed = HeatBed("HB",origin, 150, 150 ,0.2, 1, 150, 12, 0.2, 4)
heatbed.traceFootprint()



