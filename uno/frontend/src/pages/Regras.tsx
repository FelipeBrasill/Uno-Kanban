import Button from '../components/Button'
import { useNavigate } from 'react-router'

function Regras() {
  const navigate = useNavigate()

  return (
    <div className="flex flex-col items-center justify-center flex-1 bg-gray-100">
      <h1>Página em Construção</h1>
      <Button text="Voltar para Tela inicial" onClick={() => navigate("/home")} />
    </div>
  )
}

export default Regras