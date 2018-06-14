

#Standard constants
#standard temperature (°C)
STD_TEMP = 20

#copper resistivity  16.78 x 10e-6 Ω•m at at the standard temperature
CU_RES =  0.0000000168

#copper temperature coefficient 
ALPHA = 0.004041

#Define mills in mm
MILL = 0.0254

#Define 1 mill/100 as mmm
MILL_PC = 0.000254

#Define std drill size mm
DRILL = 1

#Define std pin pad diameter in mm (3.5)
PDIA = 3.5


class Conductor:
    def __init__ (self, resistivity, thermal_const):
        #resistivity of the material in Ohm.m
        self._resistivity = resistivity

        #resistance thermal constant
        self._thermal_const =  thermal_const

    """ Getter for the resistivity"""
    def getResistivity(self):
        return self._resistivity

    """ Getter for the thermal constant """
    def getThermalConst(self):
        return self._thermal_const
