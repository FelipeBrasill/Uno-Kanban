from abc import ABC

class Carta(ABC):
    '''Clase abstracta que representa una carta de UNOKAnBAN.'''
    def __init__(self, color : str):
        self.color = color

