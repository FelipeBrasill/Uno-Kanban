import { useEffect, useState } from "react"
import { useNavigate } from "react-router"
import Button from "../components/Button"
import routes_name from "../routes/routes"
import { obterNomeJogador } from "../api/JogadorAtual"
import { partidaApi, PartidaApiError } from "../api/partidaApi"

function Home() {
  const navigate = useNavigate()
  type RouteChoices = keyof typeof routes_name

  const [nomeJogador, setNomeJogador] = useState<string | null>(null)
  const [criandoPartida, setCriandoPartida] = useState(false)
  const [outrosNomes, setOutrosNomes] = useState<string[]>([""])
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

  function atualizarOutroNome(indice: number, valor: string) {
    setOutrosNomes((atual) => {
      const copia = [...atual]
      copia[indice] = valor
      return copia
    })
    if (erro) setErro(null)
  }

  function adicionarCampoJogador() {
    setOutrosNomes((atual) => [...atual, ""])
  }

  function removerCampoJogador(indice: number) {
    setOutrosNomes((atual) => atual.filter((_, i) => i !== indice))
  }

  async function handleCriarPartida() {
    if (!nomeJogador) return

    setErro(null)

    const nomesLimpos = outrosNomes.map((n) => n.trim()).filter(Boolean)
    const todosOsNomes = [nomeJogador, ...nomesLimpos]

    if (todosOsNomes.length < 2) {
      setErro("Adicione pelo menos mais um jogador.")
      return
    }

    if (new Set(todosOsNomes).size !== todosOsNomes.length) {
      setErro("Os nomes dos jogadores precisam ser únicos.")
      return
    }

    // Gerado no client: a API não expõe nenhum endpoint que gere ou reserve
    // um id de partida, então criamos um aqui mesmo.
    const idPartida = Date.now()

    setCarregando(true)
    try {
      const estadoInicial = await partidaApi.criarPartida(idPartida, todosOsNomes)
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

          {outrosNomes.map((valor, indice) => (
            <div key={indice} className="flex gap-2 w-full">
              <input
                type="text"
                value={valor}
                onChange={(e) => atualizarOutroNome(indice, e.target.value)}
                placeholder={`Nome do jogador ${indice + 2}`}
                className="flex-1 px-3 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary"
              />
              {outrosNomes.length > 1 && (
                <button
                  onClick={() => removerCampoJogador(indice)}
                  className="text-red-500 px-2"
                  aria-label="Remover jogador"
                >
                  ×
                </button>
              )}
            </div>
          ))}

          <button onClick={adicionarCampoJogador} className="text-sm text-blue-600 underline">
            + adicionar jogador
          </button>

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