import numpy as np


def tansig(n):
    return (2 / (1 + np.exp(-2 * n)) - 1)


class modelo(object):
    """docstring for modelo"""

    def __init__(self, Sexo, Edad, Clinico, Sida, Hcalle, Diabetes):

        self.Sexo = Sexo;
        self.Edad = Edad;
        self.Clinico = Clinico;
        self.Sida = Sida;
        self.Hcalle = Hcalle;
        self.Diabetes = Diabetes;


    def diagnosticar(self):
        # Cargamos los pesos de la mejor red
        IW = open("./modelo/IW.txt", "r").read()  # IW.txt es un archivo con los pesos de la red entrenada (PESOS ENTRADA)
        t = []
        for x in IW.split(";"):
            t1 = []
            for y in x.split():
                t1.append(float(y))
            t.append(t1)
        IW = t
        bL = float(
            open("./modelo/bL.txt", "r").read())
        LW = open("./modelo/LW.txt", "r").read()
        LW = [float(x) for x in LW.split()]
        bI = open("./modelo/bI.txt", "r").read()
        bI = [float(x) for x in bI.split(";")]
        bI = np.array(bI)

        # Cargamos los pesos de la mejor red
        Codebook = open('./modelo/Codebook.txt',
                        "r").read();  # Codebook.txt es un archivo con los pesos de la red SOM entrenada
        t = []
        for x in Codebook.split("\n"):
            t1 = []
            for y in x.split():
                t1.append(float(y))
            t.append(t1)
        Codebook = t

        # def diagnostico(self):

        entrada = [self.Sexo, self.Edad, self.Clinico, self.Sida, self.Hcalle, self.Diabetes]

        entrada = np.array(entrada)

        # salida = tansig((LW*tansig((IW*entrada)+bI))+bL)

        salida = tansig((np.dot(tansig((np.dot(IW, entrada.T)) + bI), LW)) + bL)

        # print("Salida del MLP: ", salida)

        # tansig((IW*entrada)+bI') primer producto punto + transpuesta del bias
        # tansig((LW*tansig((IW*entrada)+bI'))+bL)

        ## Parte del SOM
        # El mapa fue entrenado con 7 entradas. Por esta razón debemos ajustar
        if self.Sexo == 1:
            entrada2 = [entrada[0], 0]
        else:
            entrada2 = [entrada[0], 1]

        entrada = entrada.tolist()

        for i in range(0, len(entrada) - 1):
            entrada2.append(entrada[i + 1])
        entrada = entrada2

        entrada = np.array(entrada)

        MU = [0] * 12  # MU son los Match Units, es decir, con qué neurona se identifica el vector de entrada

        for i in range(0, 12):
            MU[i] = np.dot(Codebook[i], entrada.T)

        # print("Salida del SOM:", MU.index(max(MU))+1)
        salidas = {'mlp': salida, 'som': MU.index(max(MU)) + 1}

        return salidas

    # BMU = find(MU==max(MU)) # Identifica la Neurona Ganadora del SOM (Best Match Unit)"""


