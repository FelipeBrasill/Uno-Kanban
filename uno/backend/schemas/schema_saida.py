from pydantic import BaseModel
from ..models.enum import EstadoRealiEhGay, EstadoJogador, CorCarta,TipoEfeito


from uuid import UUID

class CartaSchema(BaseModel):
    id: UUID
    cor: CorCarta

class CartaComumSchema(CartaSchema):
    valor: int

class CartaAcaoSchema(CartaSchema):
    acao: TipoEfeito

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

