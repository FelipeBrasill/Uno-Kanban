from abc import ABC
from .enum import CorCarta
from abc import ABC
from uuid import uuid4, UUID
class Carta(ABC):
    '''Classe abstrata que representa uma carta de UNOKAnBAN.'''
    def __init__(self, cor: CorCarta):
        self.cor: CorCarta = cor
        self.id: UUID = uuid4()

