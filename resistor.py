
import constants

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class Resistor:
    def __init__(self, r, temp):
    
        #nominal resistance in Ohms (protected)
        self._r = r
        

    """Getter for the standard temperature that the resistance was
    meansured"""
    def getStdTemp (self):
        return self._std_temp

    def getRr(self):
        return self._r
    
    """Getter for the resistance (meansured at _std_temp temperature)"""
    def getR(self, temperature):
        return self._r*math.exp(self._thermal_const*(temperature - std_temp))
    
    def getR(self, r_std, temperature):
        return r_std*math.exp(self._thermal_const*(temperature - std_temp))

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

class WireResistor(Resistor):
    def __init__ (self, r, Temp, conductor):

        #calls the constructor of the superclass (Resistor)
        super().__init__(r, Temp)

        #define the resistor conductor
        if isinstance(conductor, constants.Conductor):
            self._conductor = conductor
        else:
            raise ValueError ("Parameter conductor is not of Conductor type")

    """ Returns the lenght of wire (in m) for the specified area (in m^2) """
    def getLenght(self, Area):
        return self._r*Area/(self._resistivity)

    """Returns the sectional are of the wire (m^2) given the lenght (m)"""
    def getArea(self, lenght):
        return (lenght*self._resistivity)/self._r

    """ Get the resistance"""
    def getR (self,lenght, area, temperature):
        return self.getR((self._resistivity*lenght/area), temperature)
    

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
        
