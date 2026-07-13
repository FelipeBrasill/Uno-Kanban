
# --- PARTIDA ---
MAO_INICIAL: int = 7
EMBARALHAR_PADRAO: int = 7
MIN_JOGADORES: int = 2
MAX_JOGADORES: int = 20
NUMERO_MAXIMO_CARTAS: int = 108
NUMERO_MINIMO_CARTAS: int = 0
BASE_NUMERICA_JOGO : int = 10
SENTIDO_PADRAO = 1
TURNO_INICIAL = 0
# --- BARALHO ---
QTD_CARTA_ZERO: int = 1      # 0 aparece 1x por cor
QTD_CARTA_NUMERO: int = 2    # 1-9 aparecem 2x por cor
QTD_CARTA_ACAO: int = 2      # cada ação aparece 2x por cor
QTD_CARTA_PRETA : int = 4
# --- REGRAS ---
QTD_COMPRA_PADRAO: int = 1       # cartas compradas ao passar a vez
QTD_COMPRA_MAIS_DOIS: int = 2    # cartas compradas por +2
QTD_COMPRA_MAIS_QUATRO: int = 4  # cartas compradas por +4 (coringa)
QTD_PUNICAO_REALIEHGAY: int = 2          # cartas compradas se não gritar REALI EH GAY

# --- BOT ---
COOLDOWN_BOT_SEGUNDOS: float = 2.0  # pausa antes de cada ação do bot, pro humano acompanhar
NOMES_BOT_DISPONIVEIS: list[str] = [
    "Benyo",
    "Reali eh Gay",
    "McLovin",
    "Calvo",
    "Felipista",
    "PT",
]