import numpy as np
from functools import reduce
from scipy.constants import pi, c, mu_0, epsilon_0
import math

class Layer:
    '''
    Assumptions:
    - All of the Layers of the anti-reflection band are lossless, non-magnetic materials, so the permeability is set to mu_0.
    - When referring to "Field," it is always the Electric field and not the Magnetic field.
    - The Width of a Layer is 1/4 the length of the wavelength propagating through the medium
    '''

    def __init__(self, indexOfRefraction:float=None, centerWaveLength:float=None, previousLayer=None):
        self.__permeability = mu_0
        self.__propagationWavelength = None
        if indexOfRefraction != None:
            self.setIndexOfRefraction(indexOfRefraction)
        else:
            self.__indexOfRefraction = None
            self.__intrinsicImpedance = None
            self.__permittivity = None
        
        if centerWaveLength != None:
            self.__computeThickness(centerWaveLength)
        else:
            self.__thickness = None
        
        if previousLayer != None:
            self.setPreviousLayer(previousLayer)
        else:
            self.__reflectionCoefficient = None
            self.__transmissionCoefficient = None
            self.__previousLayer = None
        self.__boundaryMatrix = None
        self.__propagationMatrix = None

    #-------------------------------------------Getters and Setters-------------------------------------------#

    def getPermittivity(self) -> float:
        return self.__permittivity

    def __setPermittivity(self, value: float) -> None:
        self.__permittivity = value

    def getPermeability(self) -> float:
        return self.__permeability

    def __setPermeability(self, value: float) -> None:
        self.__permeability = value

    def getPropagationWavelength(self) -> float:
        return self.__propagationWavelength

    def setPropagationWavelength(self, value: float) -> None:
        self.__propagationWavelength = value/self.getIndexOfRefraction()

    def __computeThickness(self, value:float) -> None:
        self.__setThickness(1/4*value) # Takes in the centerwavelength and divides the value by for and sets it as its thickness

    def getIndexOfRefraction(self) -> float:
        return self.__indexOfRefraction

    def setIndexOfRefraction(self, value: float) -> None:
        self.__indexOfRefraction = value
        self.__setPermittivity(math.pow(self.getIndexOfRefraction(), 2) * epsilon_0)
        self.__setIntrinsicImpedance(math.sqrt(self.getPermeability() / self.getPermittivity()))

    def getIntrinsicImpedance(self) -> float:
        return self.__intrinsicImpedance

    def __setIntrinsicImpedance(self, value: float) -> None:
        self.__intrinsicImpedance = value

    def getThickness(self) -> float:
        return self.__thickness

    def __setThickness(self, value: float) -> None:
        self.__thickness = value

    def getReflectionCoefficient(self) -> float:
        return self.__reflectionCoefficient

    def __setReflectionCoefficient(self, value: float) -> None:
        self.__reflectionCoefficient = value

    def getTransmissionCoefficient(self) -> float:
        return self.__transmissionCoefficient

    def __setTransmissionCoefficient(self, value: float) -> None:
        self.__transmissionCoefficient = value

    def getPreviousLayer(self):
        return self.__previousLayer
    
    def getBoundaryMatrix(self) -> float:
        return self.__boundaryMatrix

    def __setBoundaryMatrix(self, value: float) -> None:
        self.__boundaryMatrix = value

    def getPropagationMatrix(self) -> float:
        return self.__propagationMatrix

    def __setPropagationMatrix(self, value: float) -> None:
        self.__propagationMatrix = value

    def setPreviousLayer(self, value):
        self.__previousLayer = value
        self.setPropagationWavelength(self.getPreviousLayer().getPropagationWavelength()*
            self.getPreviousLayer().getIndexOfRefraction() / self.getIndexOfRefraction())
        self.__setReflectionCoefficient(
            (self.getPreviousLayer().getIntrinsicImpedance() - self.getIntrinsicImpedance()) /
            (self.getPreviousLayer().getIntrinsicImpedance() + self.getIntrinsicImpedance())
        )
        self.__setTransmissionCoefficient(
            (self.getPreviousLayer().getIntrinsicImpedance() * 2) /
            (self.getPreviousLayer().getIntrinsicImpedance() + self.getIntrinsicImpedance())
        )
    
    def computeBoundaryMatrix(self):
        try:
            if self.getReflectionCoefficient() == None:
                raise ValueError("Reflection Coefficient was not initialized")

            if self.getTransmissionCoefficient() == None:
                raise ValueError("Transmission Coefficient was not initialized")
        except ValueError as e:
            raise e
        else:
            self.__setBoundaryMatrix(1/(self.getTransmissionCoefficient())*
            (np.matrix([[1, self.getReflectionCoefficient()], [self.getReflectionCoefficient(), 1]], dtype='complex_')))

    def computePropagationMatrix(self):
        try:
            if self.getPropagationWavelength() == None:
                raise ValueError("Wavelength was not initialized")

        except ValueError as e:
            raise e
        else:
            phaseThickness = 2*pi*self.getIndexOfRefraction()*self.getThickness()/self.getPropagationWavelength()
            self.__setPropagationMatrix(
                np.array([[math.e**(1j*phaseThickness), 0] , [0, math.e**(-1j*phaseThickness)]], dtype='complex_')
            )
            
            
    #-------------------------------------------Computations-------------------------------------------#


if __name__ == "__main__":
    layer1 = Layer(1, 650*math.pow(10, -9), None)
    layer1.setPropagationWavelength(650*math.pow(10, -9))

    layer2 = Layer(1, 650*math.pow(10, -9), layer1)
    layer2.computeBoundaryMatrix()
    layer2.computePropagationMatrix()

    layer3 = Layer(3.5, 650*math.pow(10, -9), layer2)
    layer3.computeBoundaryMatrix()

    T = reduce(np.dot, [layer2.getBoundaryMatrix(), layer2.getPropagationMatrix(), layer3.getBoundaryMatrix()]) # Applies the matrix multiplication for 2 layers and a boundary

    reflectionCoefficient = T[1,0]/T[0,0]
    transmissionCoefficient = 1/T[0,0]

    reflectivity = math.pow(np.abs(reflectionCoefficient), 2)
    transmittivity = math.pow(np.abs(transmissionCoefficient), 2)*(1/3.5)

    pass