from pydantic import BaseModel
from uno.backend.models.enum import EstadoRealiEhGay, EstadoJogador


class CartaSchema(BaseModel):
    cor: str


class CartaComumSchema(CartaSchema):
    valor: int


class CartaAcaoSchema(CartaSchema):
    efeito: str


class JogadorSchema(BaseModel):
    nome:              str
    quantidade_cartas: int
    estado_realiehgay: EstadoRealiEhGay
    estado_jogador:    EstadoJogador


class MaoSchema(BaseModel):
    mao: list[CartaComumSchema | CartaAcaoSchema]


class EstadoPartidaSchema(BaseModel):
    jogador_atual: JogadorSchema
    vencedor:      JogadorSchema | None = None
    carta_topo:    CartaComumSchema | CartaAcaoSchema
    jogadores:     list[JogadorSchema]