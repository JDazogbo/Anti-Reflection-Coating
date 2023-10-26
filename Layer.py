import numpy as np
from functools import reduce
from scipy.constants import pi, c, mu_0, epsilon_0
import math

class Layer:
    ''' Object representation of a layer and the boundary that precedes it.

    Args:
        indexOfRefraction(float): Index of refraction of the layer. Defaults to None.
        centerWaveLength(float): Center wavelength that is optimized for maximum transmission. The thickness
            of the medium is derived from this value. Defaults to None.
        previousLayer(Layer): Layer that creates the incident fields for the current media.
            The reflection/transmission coefficients are derived with this object. Defaults to None.

    Media Assumptions:
        - All of the layers of the anti-reflection band are lossless, non-magnetic materials, so the permeability is set to mu_0.
        - When referring to "Field," it is always the Electric field and not the Magnetic field.
        - The width of a layer is 1/4 the length of the wavelength propagating through the medium.
    '''

    #-------------------------Constructor-------------------------#

    def __init__(self, indexOfRefraction: float = None, centerWaveLength: float = None, previousLayer=None):
        self.__permeability = mu_0
        self.__propagationWavelength = None

        if indexOfRefraction is not None:
            self.setIndexOfRefraction(indexOfRefraction)
        else:
            self.__indexOfRefraction = None
            self.__intrinsicImpedance = None
            self.__permittivity = None
        
        if previousLayer is not None:
            self.setPreviousLayer(previousLayer)
        else:
            self.__reflectionCoefficient = None
            self.__transmissionCoefficient = None
            self.__previousLayer = None

        if centerWaveLength is not None:
            self.__computeThickness(centerWaveLength)
        else:
            self.__thickness = None

        self.__boundaryMatrix = None
        self.__propagationMatrix = None

    #-------------------------Getters and Setters-------------------------#

    def getPermittivity(self) -> float:
        '''Returns the permittivity (epsilon) of the current layer.
        Returns:
            float: Permittivity of the layer.
        '''
        return self.__permittivity

    def __setPermittivity(self, value: float) -> None:
        '''Sets the permittivity (epsilon) of the current layer.
        Args:
            value(float): Permittivity to be set to the layer.
        '''
        self.__permittivity = value

    def getPermeability(self) -> float:
        '''Returns the permeability of the current layer (mu_0).
        Returns:
            float: Permeability of the layer (mu_0).
        '''
        return self.__permeability

    def __setPermeability(self, value: float) -> None:
        '''Sets the permeability of the current layer (mu_0).
        Args:
            value(float): Permeability (mu_0) to be set to the layer.
        '''
        self.__permeability = value

    def getPropagationWavelength(self) -> float:
        '''Returns the propagation wavelength of the current layer.
        Returns:
            float: Propagation wavelength of the layer.
        '''
        return self.__propagationWavelength

    def setPropagationWavelength(self, value: float) -> None:
        '''Sets the propagation wavelength of the current layer.
        Args:
            value(float): Propagation wavelength to be set to the layer.
        '''
        self.__propagationWavelength = value
        
    def __computeThickness(self, value: float) -> None:
        '''Computes the thickness of the layer based on the center wavelength.
        Args:
            value(float): Center wavelength used to compute the thickness.
        '''
        if self.getPreviousLayer() == None:
            self.__setThickness(value / (4 *self.getIndexOfRefraction()))
        else:
            self.__setThickness(value / (4 *self.getIndexOfRefraction())*self.getPreviousLayer().getIndexOfRefraction())

    def getIndexOfRefraction(self) -> float:
        '''Returns the index of refraction of the current layer.
        Returns:
            float: Index of refraction of the layer.
        '''
        return self.__indexOfRefraction

    def setIndexOfRefraction(self, value: float) -> None:
        '''Sets the index of refraction of the current layer and derives related properties.
        Args:
            value(float): Index of refraction to be set to the layer.
        '''
        self.__indexOfRefraction = value
        self.__setPermittivity(math.pow(self.getIndexOfRefraction(), 2) * epsilon_0)
        self.__setIntrinsicImpedance(math.sqrt(self.getPermeability() / self.getPermittivity()))

    def getIntrinsicImpedance(self) -> float:
        '''Returns the intrinsic impedance of the current layer.
        Returns:
            float: Intrinsic impedance of the layer.
        '''
        return self.__intrinsicImpedance

    def __setIntrinsicImpedance(self, value: float) -> None:
        '''Sets the intrinsic impedance of the current layer.
        Args:
            value(float): Intrinsic impedance to be set to the layer.
        '''
        self.__intrinsicImpedance = value

    def getThickness(self) -> float:
        '''Returns the thickness of the current layer.
        Returns:
            float: Thickness of the layer.
        '''
        return self.__thickness

    def __setThickness(self, value: float) -> None:
        '''Sets the thickness of the current layer.
        Args:
            value(float): Thickness to be set to the layer.
        '''
        self.__thickness = value

    def getReflectionCoefficient(self) -> float:
        '''Returns the reflection coefficient of the current layer.
        Returns:
            float: Reflection coefficient of the layer.
        '''
        return self.__reflectionCoefficient

    def __setReflectionCoefficient(self, value: float) -> None:
        '''Sets the reflection coefficient of the current layer.
        Args:
            value(float): Reflection coefficient to be set to the layer.
        '''
        self.__reflectionCoefficient = value

    def getTransmissionCoefficient(self) -> float:
        '''Returns the transmission coefficient of the current layer.
        Returns:
            float: Transmission coefficient of the layer.
        '''
        return self.__transmissionCoefficient

    def __setTransmissionCoefficient(self, value: float) -> None:
        '''Sets the transmission coefficient of the current layer.
        Args:
            value(float): Transmission coefficient to be set to the layer.
        '''
        self.__transmissionCoefficient = value

    def getPreviousLayer(self):
        '''Returns the previous layer.
        Returns:
            Layer: The previous layer.
        '''
        return self.__previousLayer

    def getBoundaryMatrix(self) -> float:
        '''Returns the boundary matrix of the current layer.
        Returns:
            float: Boundary matrix of the layer.
        '''
        return self.__boundaryMatrix

    def __setBoundaryMatrix(self, value: float) -> None:
        '''Sets the boundary matrix of the current layer.
        Args:
            value(float): Boundary matrix to be set to the layer.
        '''
        self.__boundaryMatrix = value

    def getPropagationMatrix(self) -> float:
        '''Returns the propagation matrix of the current layer.
        Returns:
            float: Propagation matrix of the layer.
        '''
        return self.__propagationMatrix

    def __setPropagationMatrix(self, value: float) -> None:
        '''Sets the propagation matrix of the current layer.
        Args:
            value(float): Propagation matrix to be set to the layer.
        '''
        self.__propagationMatrix = value

    def setPreviousLayer(self, value):
        '''Sets the previous layer and computes related properties.
        Args:
            value(Layer): The previous layer to be set.
        '''
        self.__previousLayer = value
        self.setPropagationWavelength(self.getPreviousLayer().getPropagationWavelength() *
                                     self.getPreviousLayer().getIndexOfRefraction())
        self.__setReflectionCoefficient(
            (self.getPreviousLayer().getIntrinsicImpedance() - self.getIntrinsicImpedance()) /
            (self.getPreviousLayer().getIntrinsicImpedance() + self.getIntrinsicImpedance())
        )
        self.__setTransmissionCoefficient(
            (self.getPreviousLayer().getIntrinsicImpedance() * 2) /
            (self.getPreviousLayer().getIntrinsicImpedance() + self.getIntrinsicImpedance())
        )

    #-------------------------Computations-------------------------#

    def computeBoundaryMatrix(self):
        try:
            if self.getReflectionCoefficient() is None:
                raise ValueError("Reflection Coefficient was not initialized")

            if self.getTransmissionCoefficient() is None:
                raise ValueError("Transmission Coefficient was not initialized")
        except ValueError as e:
            raise e
        else:
            self.__setBoundaryMatrix(1 / (self.getTransmissionCoefficient()) *
            (np.matrix([[1, self.getReflectionCoefficient()], [self.getReflectionCoefficient(), 1]], dtype='complex_')))

    def computePropagationMatrix(self):
        try:
            if self.getPropagationWavelength() is None:
                raise ValueError("Wavelength was not initialized")
        except ValueError as e:
            raise e
        else:
            phaseThickness = 2 * pi *  self.getThickness() / (self.getPropagationWavelength()) * self.getIndexOfRefraction()
            self.__setPropagationMatrix(
                np.array([[math.e**(1j * phaseThickness), 0], [0, math.e**(-1j * phaseThickness)]], dtype='complex_')
            )
