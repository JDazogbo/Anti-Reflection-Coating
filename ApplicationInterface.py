import numpy as np
from functools import reduce
from scipy.constants import pi, c, mu_0, epsilon_0
import math
from Layer import Layer
import matplotlib.pyplot as plt

def prompt(inputMessage:str, errorMessage:str, valType):
    while True:
        try:
            value = input(inputMessage + ": ")
            return valType(value)
        except ValueError as e:
            print(errorMessage)

def reflecticityWavelengthCalculator(wavelengths, centerWaveLength, indexOfRefractions):
    reflectivities = []
    for wavelength in wavelengths:
        layers = []
        for i in range(0, len(indexOfRefractions)):
            if i == 0:
                layers.append(Layer(indexOfRefractions[i], centerWaveLength, None))
                layers[i].setPropagationWavelength(wavelength*math.pow(10, -9))
            else:
                layers.append(Layer(indexOfRefractions[i], centerWaveLength, layers[i-1]))
                layers[i].computeBoundaryMatrix()
                layers[i].computePropagationMatrix()
        liste = []
        for i in range(1, len(layers)-1):
            liste.append(layers[i].getBoundaryMatrix())
            liste.append(layers[i].getPropagationMatrix())
        liste.append(layers[len(layers)-1].getBoundaryMatrix())
        T = reduce(np.dot, liste)
        
        reflectionCoefficient = T[1, 0] / T[0, 0]

        reflectivity = math.pow(np.abs(reflectionCoefficient), 2)
        
        reflectivities.append(reflectivity*100)
    return reflectivities


if __name__ =="__main__":
    
    while True:
        try:
            useCase = prompt('''Select the corresponding option to the use case of this tool:\n   1) Graphing Tool\n   2) Reflectivity/Transmittivity Calculator\nOption''', "Value is not an Integer", int)
            if useCase == 1:
                layerNumber = prompt("Input the number of layers", "Value is not an Integer", int)
                indexOfRefractions = []
                for i in range(layerNumber):
                    indexOfRefractions.append(prompt("Input the Index of Refraction for layer {index}".format(index = i), "Value is not a float", float))

                centerWaveLength = prompt("Input the center wave length in nanometers", "Value is not a float", float)*math.pow(10, -9)
                lowerWavelength = prompt("Input the lower bound wave length in nanometers", "Value is not a float", float)*math.pow(10, -9)
                higherWavelength = prompt("Input the higher bound wave length in nanometers", "Value is not a float", float)*math.pow(10, -9)

                wavelengths = range(int(lowerWavelength*math.pow(10, 9)), int(higherWavelength*math.pow(10, 9)), 1)
                reflectivities = reflecticityWavelengthCalculator(wavelengths, centerWaveLength, indexOfRefractions)

                plt.plot(wavelengths, reflectivities)
                plt.title("Reflecticity as a function of Wavelength")
                plt.xlabel("Wavelenegth (in nanometers)")
                plt.ylabel("Reflecticity (in Percentage)")
                plt.show()
                break
            elif useCase ==2:
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

                liste = []
                for i in range(1, len(layers)-1):
                    liste.append(layers[i].getBoundaryMatrix())
                    liste.append(layers[i].getPropagationMatrix())
                liste.append(layers[len(layers)-1].getBoundaryMatrix())
                T = reduce(np.dot, liste)

                reflectionCoefficient = T[1, 0] / T[0, 0]
                transmissionCoefficient = 1 / T[0, 0]

                reflectivity = math.pow(np.abs(reflectionCoefficient), 2)
                transmittivity = math.pow(np.abs(transmissionCoefficient), 2) * (layers[0].getIndexOfRefraction()/layers[len(layers)-1].getIndexOfRefraction())
                
                print("Reflectivity: {reflectivity:.2f}%\nTransmittivity: {transmittivity:.2f}%\n\nTransfer Matrix: {TMM}".format(reflectivity = 100*reflectivity, transmittivity = 100*transmittivity, TMM = T))
                break
            else:
                raise ValueError("Value is not in the selectable options")
        except ValueError as e:
            print(e)


    
