from abc import ABC
from .enum import CorCarta
class Carta(ABC):
    '''Clase abstrata que representa una carta de UNOKAnBAN.'''
    def __init__(self, cor : CorCarta):
        self.cor : CorCarta = cor

