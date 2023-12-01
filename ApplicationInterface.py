import numpy as np
from functools import reduce
from scipy.constants import pi, c, mu_0, epsilon_0
from scipy import integrate
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

def reflecticitySingleWavelengthCalculator(wavelength, indexOfRefractions):
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

    return math.pow(np.abs(reflectionCoefficient), 2)
    

def irradianceCalculator(wavelength):
    return (6.16*math.pow(10, 15))/(math.pow(wavelength, 5)*(math.exp(2484/wavelength)-1))


if __name__ =="__main__":
    
    while True:
        try:
            useCase = prompt('''Select the corresponding option to the use case of this tool:\n   
1) Graphing Tool (Part 2)\n   
2) Reflectivity/Transmittivity Calculator (Part 1)\n
3) Triple Layer Power Calculator (Part 4)\n
Option''', "Value is not an Integer", int)
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
                
                plt.xlabel("Wavelenegth (in nanometers)")
                plt.ylabel("Reflecticity (in Percentage)")

                power = integrate.quad(lambda x: irradianceCalculator(x)*(1-reflecticitySingleWavelengthCalculator(x, indexOfRefractions)), wavelengths[0], wavelengths[len(wavelengths)-1])
                plt.title("Reflecticity as a function of Wavelength\nPower Production: {power:.2f} ± {uncertainty:.2f}".format(power = power[0], uncertainty = power[1]))
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
            elif useCase ==3:
                indexOfRefractions = [1, 1.4, None, 3.15, 3.5]

                centerWaveLength = 650
                lowerWavelength = 200
                higherWavelength = 2200
                wavelengths = range(lowerWavelength, higherWavelength, 1)

                powers = []

                for i in np.arange(1.4, 3, 0.05):
                    indexOfRefractions[2] = i
                    power = integrate.quad(lambda x: irradianceCalculator(x)*(1-reflecticitySingleWavelengthCalculator(x, indexOfRefractions)), wavelengths[0], wavelengths[len(wavelengths)-1], limit=150)
                    powers.append(power[0])
                
                plt.plot(np.arange(1.4, 3, 0.05), powers)
                
                plt.xlabel("Choice of Index of Refraction for Layer 2")
                plt.ylabel("Received Power")

                plt.title("Power received as a function of Index of Refractions of Layers 2")
                plt.show()

            else:
                raise ValueError("Value is not in the selectable options")
        except ValueError as e:
            print(e)


    
