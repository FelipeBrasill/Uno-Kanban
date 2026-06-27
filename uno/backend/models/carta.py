from abc import ABC

class Carta(ABC):
    '''Clase abstrata que representa una carta de UNOKAnBAN.'''
    def __init__(self, cor : str):
        self.color = cor

