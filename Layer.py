import numpy as np
from scipy.constants import pi, c, mu_0, epsilon_0
import math

class Layer:
    '''
    Assumptions:
    - All of the Layers of the anti-reflection band are lossless, non-magnetic materials, so the permeability is set to mu_0.
    - When referring to "Field," it is always the Electric field and not the Magnetic field.
    '''

    def __init__(self):
        self.__permittivity = None
        self.__permeability = mu_0
        self.__propagationWavelength = None
        self.__indexOfRefraction = None
        self.__intrinsicImpedance = None
        self.__thickness = None
        self.__reflectionCoefficient = None
        self.__transmissionCoefficient = None
        self.__incidentField = None
        self.__reflectedField = None
        self.__transmittedField = None
        self.__transflectedField = None
        self.__previousLayer = None

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
        self.__propagationWavelength = value

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

    def setThickness(self, value: float) -> None:
        self.__thickness = value

    def getReflectionCoefficient(self) -> float:
        return self.__reflectionCoefficient

    def __setReflectionCoefficient(self, value: float) -> None:
        self.__reflectionCoefficient = value

    def getTransmissionCoefficient(self) -> float:
        return self.__transmissionCoefficient

    def __setTransmissionCoefficient(self, value: float) -> None:
        self.__transmissionCoefficient = value

    def getIncidentField(self) -> float:
        return self.__incidentField

    def setIncidentElectricField(self, value: float) -> None:
        self.__incidentField = value

    def getReflectedField(self) -> float:
        return self.__reflectedField

    def setReflectedField(self, value: float) -> None:
        self.__reflectedField = value

    def getTransmittedField(self) -> float:
        return self.__transmittedField

    def setTransmittedField(self, value: float) -> None:
        self.__transmittedField = value

    def getTransflectedField(self) -> float:
        return self.__transflectedField

    def setTransflectedField(self, value: float) -> None:
        self.__transflectedField = value

    def getPreviousLayer(self):
        return self.__previousLayer

    def setPreviousLayer(self, value):
        self.__previousLayer = value
        self.setPropagationWavelength(self.getPreviousLayer().getPropagationWavelength() / self.getIndexOfRefraction())
        self.__setReflectionCoefficient(
            (self.getPreviousLayer().getIntrinsicImpedance() - self.getIntrinsicImpedance()) /
            (self.getPreviousLayer().getIntrinsicImpedance() + self.getIntrinsicImpedance())
        )
        self.__setTransmissionCoefficient(
            (self.getPreviousLayer().getIntrinsicImpedance() * 2) /
            (self.getPreviousLayer().getIntrinsicImpedance() + self.getIntrinsicImpedance())
        )
    
    #-------------------------------------------Computations-------------------------------------------#


if __name__ == "__main__":
    layer1 = Layer()
    layer1.setIndexOfRefraction(1)
    layer1.setPropagationWavelength(650*math.pow(10, -9))

    layer2 = Layer()
    layer2.setIndexOfRefraction(3.5)
    layer2.setPreviousLayer(layer1)
    pass