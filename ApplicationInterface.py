import numpy as np
from functools import reduce
from scipy.constants import pi, c, mu_0, epsilon_0
import math
from Layer import Layer

def prompt(inputMessage:str, errorMessage:str, valType):
    while True:
        try:
            value = input(inputMessage + ": ")
            return valType(value)
        except ValueError as e:
            print(errorMessage)



if __name__ =="__main__":
    
    layerNumber = prompt("Input the number of layers", "Value is not an Integer", int)
    centerWaveLength = prompt("Input the center wave length in nanometers", "Value is not a float", float)*math.pow(10, -9)
    layers = []
    for i in range(0, layerNumber):
        print()
        if i == 0:
            indexOfRefraction = prompt("Input the Index of Refraction for layer {index}".format(index = i), "Value is not a float", float)
            propagationWavelength = prompt("Input the initial propagation wave length for layer {index} in nanometers".format(index = i), "Value is not a float", float)
            layers.append(Layer(indexOfRefraction, centerWaveLength, None))
            layers[i].setPropagationWavelength(propagationWavelength)
        else:
            indexOfRefraction = prompt("Input the Index of Refraction for layer {index}".format(index = i), "Value is not a float", float)
            layers.append(Layer(indexOfRefraction, centerWaveLength, layers[i-1]))
            layers[i].setPropagationWavelength(propagationWavelength)
            layers[i].computeBoundaryMatrix()
            layers[i].computePropagationMatrix()

    T = reduce(np.dot, [layers[i].getBoundaryMatrix() for i in range(1, len(layers)-1)] + [layers[i].getPropagationMatrix() for i in range(1, len(layers)-1)]+ [layers[len(layers)-1].getBoundaryMatrix()])
    
    reflectionCoefficient = T[1, 0] / T[0, 0]
    transmissionCoefficient = 1 / T[0, 0]

    reflectivity = math.pow(np.abs(reflectionCoefficient), 2)
    transmittivity = math.pow(np.abs(transmissionCoefficient), 2) * (1 / 3.5)
    print("Reflectivity: {reflectivity:.2f}%\nTransmittivity: {transmittivity:.2f}%\n\nTransfer Matrix: {TMM}".format(reflectivity = 100*reflectivity, transmittivity = 100*transmittivity, TMM = T))