import BgImage from '../assets/bg_login.png'
import Button from '../components/Button'

import { useNavigate } from 'react-router'
import { useState } from 'react'

function Login() {
  const navigate = useNavigate()
  const [nome, setNome] = useState('')

  const handleLogin = () => {
    console.log('Nome do usuário:', nome)
    navigate('/home')
  }

  return (
    <div className="relative min-h-screen flex items-start justify-center overflow-hidden pt-32">
      <div
        className="absolute inset-0 bg-cover bg-center blur-[2px] scale-110"
        style={{ backgroundImage: `url(${BgImage})` }}
      />

      {/* Conteúdo central */}
      <div className="relative z-10 flex flex-col items-center text-center px-4 ">
        <h1 className="text-black text-6xl md:text-9xl font-bold mb-2">
          Kubuno
        </h1>
        <p className="text-black/80 text-base md:text-lg mb-8">
          O verdadeiro jogo de cartas do Kanban!
        </p>

        <input
          type="text"
          value={nome}
          onChange={(e) => setNome(e.target.value)}
          placeholder="Digite seu nome"
          className="mb-4 px-4 py-2 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent"
        />

        <Button text="Entrar" onClick={handleLogin} />
      </div>
    </div>
  )
}

export default Login