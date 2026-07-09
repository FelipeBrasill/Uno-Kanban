/**
 * Helper temporário pra guardar/recuperar o nome do jogador atual.
 *
 * ASSUMIDO: ainda não existe um Contexto/estado global no projeto, então
 * usamos localStorage como solução simples pra "lembrar" o nome entre as
 * telas (Login -> Inicial -> Partida). Quando o grupo criar um
 * JogadorContext de verdade, essas duas funções podem virar chamadas de
 * contexto sem precisar mudar quem as usa.
 */

const CHAVE_NOME_JOGADOR = 'kubuno:nomeJogador'

export function salvarNomeJogador(nome: string): void {
  localStorage.setItem(CHAVE_NOME_JOGADOR, nome)
}

export function obterNomeJogador(): string | null {
  return localStorage.getItem(CHAVE_NOME_JOGADOR)
}