import BgImage from '../assets/bg/bg_login.png'
import Button from '../components/Button'

import { useNavigate } from 'react-router'
import { useState } from 'react'
import { salvarNomeJogador } from '../api/JogadorAtual.ts'
import routes_name from '../routes/routes.ts'

function Login() {
  const navigate = useNavigate()
  const [nome, setNome] = useState('')
  const [erro, setErro] = useState<string | null>(null)

  const handleLogin = () => {
    const nomeLimpo = nome.trim()

    if (!nomeLimpo) {
      setErro('Digite um nome pra continuar.')
      return
    }

    salvarNomeJogador(nomeLimpo)
    navigate(routes_name.home)
  }

  return (
    <div className="relative min-h-screen flex items-start justify-center overflow-hidden pt-32">
      <div
        className="absolute inset-0 bg-cover bg-center blur-[2px] scale-110"
        style={{ backgroundImage: `url(${BgImage})` }}
      />

      {/* Conteúdo central */}
      <div className="relative z-10 flex flex-col items-center text-center pd-4 ">
        <h1 className="text-black text-6xl md:text-9xl font-bold mb-2">
          KUBUNO
        </h1>
        <p className="text-black/80 text-base md:text-lg mb-8">
          O verdadeiro jogo de cartas do Kanban!
        </p>

        <input
          type="text"
          value={nome}
          onChange={(e) => {
            setNome(e.target.value)
            if (erro) setErro(null)
          }}
          placeholder="Digite seu nome"
          className="mb-2 px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
        />

        {erro && <p className="text-red-600 text-sm mb-2">{erro}</p>}

        <Button text="Entrar" onClick={handleLogin} />
      </div>
    </div>
  )
}

export default Login