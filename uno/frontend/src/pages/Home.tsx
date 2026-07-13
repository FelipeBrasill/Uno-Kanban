import { useEffect, useState } from "react"
import { useNavigate } from "react-router"
import Button from "../components/Button"
import routes_name from "../routes/routes"
import { obterNomeJogador } from "../api/JogadorAtual"
import { partidaApi, PartidaApiError } from "../api/partidaApi"

// Espelha backend/models/config.py (MIN_JOGADORES / MAX_JOGADORES). Não há
// endpoint que exponha essas constantes, então duplicamos aqui -- se o
// grupo mudar os limites no backend, precisa lembrar de atualizar isso.
const MIN_JOGADORES = 2
const MAX_JOGADORES = 20
const MIN_BOTS = MIN_JOGADORES - 1 // 1 bot, já que o humano ocupa uma vaga
const MAX_BOTS = MAX_JOGADORES - 1

function Home() {
  const navigate = useNavigate()
  type RouteChoices = keyof typeof routes_name

  const [nomeJogador, setNomeJogador] = useState<string | null>(null)
  const [criandoPartida, setCriandoPartida] = useState(false)
  const [quantidadeBots, setQuantidadeBots] = useState(MIN_BOTS)
  const [erro, setErro] = useState<string | null>(null)
  const [carregando, setCarregando] = useState(false)

  // Se não existe nome salvo, o jogador nunca passou pela Tela Login
  // (ou o localStorage foi limpo) -- manda de volta pra lá.
  useEffect(() => {
    const nome = obterNomeJogador()
    if (!nome) {
      navigate(routes_name.login)
      return
    }
    setNomeJogador(nome)
  }, [navigate])

  const choiceRouter = (choice: RouteChoices) => {
    if (choice in routes_name) {
      navigate(`${routes_name[choice]}`)
    } else {
      console.error(`Invalid route choice: ${choice}`)
    }
  }

  function ajustarQuantidadeBots(delta: number) {
    setQuantidadeBots((atual) => {
      const novo = atual + delta
      if (novo < MIN_BOTS || novo > MAX_BOTS) return atual
      return novo
    })
    if (erro) setErro(null)
  }

  async function handleCriarPartida() {
    if (!nomeJogador) return

    setErro(null)

    // Gerado no client: a API não expõe nenhum endpoint que gere ou reserve
    // um id de partida, então criamos um aqui mesmo.
    const idPartida = Date.now()

    setCarregando(true)
    try {
      const estadoInicial = await partidaApi.criarPartida(idPartida, nomeJogador, quantidadeBots)
      // CONFIRMADO pelo AppRoutes.tsx: a rota de partida é fixa, "/partida",
      // sem parâmetro de id na URL. Por isso o idPartida vai junto no state
      // da navegação, não na URL -- a Tela Partida precisa ler
      // `location.state.idPartida` (via useLocation), não `useParams`.
      navigate(routes_name.partida, { state: { idPartida, estadoInicial } })
    } catch (e) {
      const mensagem = e instanceof PartidaApiError ? e.message : "Erro ao criar partida."
      setErro(mensagem)
    } finally {
      setCarregando(false)
    }
  }

  if (!nomeJogador) {
    // Evita "piscar" a tela antes do redirect do useEffect
    return null
  }

  return (
    <div className="flex flex-col items-center justify-center flex-1 bg-gray-100 gap-4 p-4">
      {!criandoPartida ? (
        <>
          <Button text="Nova Partida" onClick={() => setCriandoPartida(true)} />
          <Button text="Regras" onClick={() => choiceRouter("regras")} />
          <Button text="Voltar para Tela de Login" onClick={() => choiceRouter("login")} />
        </>
      ) : (
        <div className="flex flex-col items-center gap-3 bg-white p-6 rounded-lg shadow-md w-full max-w-sm">
          <h2 className="text-xl font-bold">Nova Partida</h2>
          <p className="text-sm text-gray-600">Jogando como: {nomeJogador}</p>

          <p className="text-sm text-gray-600">Quantos bots vão jogar com você?</p>

          <div className="flex items-center gap-4">
            <button
              onClick={() => ajustarQuantidadeBots(-1)}
              disabled={quantidadeBots <= MIN_BOTS}
              className="w-10 h-10 rounded-full border border-gray-300 text-xl font-bold disabled:opacity-40"
              aria-label="Diminuir quantidade de bots"
            >
              −
            </button>
            <span className="text-2xl font-bold w-8 text-center">{quantidadeBots}</span>
            <button
              onClick={() => ajustarQuantidadeBots(1)}
              disabled={quantidadeBots >= MAX_BOTS}
              className="w-10 h-10 rounded-full border border-gray-300 text-xl font-bold disabled:opacity-40"
              aria-label="Aumentar quantidade de bots"
            >
              +
            </button>
          </div>

          {erro && <p className="text-red-600 text-sm">{erro}</p>}

          <div className="flex gap-2 mt-2">
            <Button
              text={carregando ? "Criando..." : "Criar Partida"}
              onClick={handleCriarPartida}
            />
            <Button text="Cancelar" onClick={() => setCriandoPartida(false)} />
          </div>
        </div>
      )}
    </div>
  )
}

export default Home