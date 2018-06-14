#!/usr/bin/python3


import math
import constants
import resistor


class HeatBed (resistor.WireResistor):

    """ 
        METHOD: CONSTRUCTOR:
        VARIABLES:
            material: conductir of wich the resistor is made. (see Class conductor in constants)
            power: the desired output power. Meansured in Watts.
            voltage: the nominal operating voltage. Meansured in  Volts.
            width: the width of the board. Meansured in mm.
            height: the height of the board. Meansured in mm.
            thickness: the conductive layer thickness. Meansured in mm.
            border: the delineating border for the board. Meansured in mm.
    """
    def __init__(self, material, power, voltage, width, height, thickness, border):

        #Calls the superclass constructor
        super().__init__(math.pow(voltage, 2)/power, constants.STD_TEMP, material)
        
    
        # Reference point for internal components
        self._x0 = self.__mmToMeter(border)
        self._y0 = self.__mmToMeter(border)
        
        #usable width and height starting at the reference points
        self._h = self.__mmToMeter(height - 2*border)
        self._w = self.__mmToMeter(width - 2*border)
        
        if thickness <= 0: raise ValueError ("Thickness should be greather than 0")
        self._thickness = self.__mmToMeter(thickness)
        
    #---------------------------------------HELPER FUNCTIONS-------------------------------
    """ converts mm to meter"""
    def __mmToMeter (self, distance):
        return distance*1.0/1000
    
    """ return the resistivity per thickness constant (betha is in ohms)"""
    def __getBetha (self):
        return (self._conductor.getResistivity()/self._thickness)
    
    
    """angular coefficient of the track width function"""
    def getU (self, b):
        betha = self.__getBetha()
        return (4*betha*b/(2*self._r + betha*math.pi))
        
    """linear coefficient of the track width function"""
    def getV (self):
        
         betha = self.__getBetha()
         return (betha*math.pi*self._h/(2*self._r + betha*math.pi))
     
    
    """ METHOD:return the track width
        VARIABLES: 
            b: the straight part of the tracks lenght: Meansured in mm.
            m: the number of track pairs (should be greathar than or equal 1).
    """
    def getW (self, b, m):
        
        
        #calculate the coefficients
        u = self.getU (b)
        v = self.getV ()
        return (u*m + v)
    
    
    
    
    
    
    
   
    """ METHOD:return the number of track pairs
        VARIABLES: 
            b: the straight part of the tracks lenght: Meansured in mm.
    """
    def getM (self, b):

        #calculate the coefficients
        u = self.getU (b)
        v = self.getV ()

        deltha = math.pow(4*v - u ,2) + 16*u*(v+self._h)
        m = ((u - 4*v) + math.sqrt(deltha))/(8*u)
        
        if (m < 1):
            raise ValueError ("Number or tracks is zero or is not even")
        
        elif m.is_integer():    #the greater integer that is less than m
            return m - 1
        else:
            return math.floor(m)
        
        
    """ METHOD:return the void width/track width constant
        VARIABLES: 
            b: the straight part of the tracks lenght: Meansured in mm.
            m: the number of track pairs (should be greathar than or equal 1).
    """
    def getK(self, b, m):
        
        #gets the track width
        w = self.getW(b,m)
        
        return (self._h - 2*m*w)/(w*(2*m - 1))
    
    #-----------------------------------------THE FUNCTION TO BE USED ON SECANT METHOD to find optimum b-----------------------------
    def function(self, b):

        #get the number of pairs
        m = self.getM(b)
        
        
        return (b + (1+ self.getK (b ,m))*self.getW(b, m) - self._w)
    
    
    def secantX (self, b_zero, b_one, iterations):

        
        b_two = 0
        for i in range (0, iterations):
            
            #calculate the function at the points b (n-1) and b(n)
            f_zero = self.function (b_zero)
            f_one =  self.function (b_one)


            #reached the point
            if f_one - f_zero == 0:
                return b_one;
                break
            
            #calculate the b(n+1)
            b_two  = b_one - (( b_one - b_zero)/(f_one - f_zero))*f_one
            
            
            b_zero = b_one
            b_one = b_two
            
        return b_one


    def r(self, b, m, w):
        betha = self.__getBetha()
        return (betha*(4*m*b +math.pi*self._h))/(2*w)
    
    

            

copper = constants.Conductor (constants.CU_RES,constants.ALPHA)
hb = HeatBed (copper, 50, 12, 150, 150, 0.1, 0)
b = hb.secantX(0.001, 0.15, 1000)
m = hb.getM(b)
w = hb.getW(b,m)
k = hb.getK(b,m)
we = k*w


print ("R:" + str (hb.r(b,m,w)))
print ("b:"+str(b))
print ("w:"+str(w))
print ("we:"+str(we)) 
print ("k:"+str(k))
print ("m:"+str(m))
        
        
        

        
        

        



