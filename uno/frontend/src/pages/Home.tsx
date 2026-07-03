import Button from "../components/Button"
import { useNavigate } from "react-router"
import routes_name from "../routes/routes"

function Home() {
  const navigate = useNavigate()
  type RouteChoices = keyof typeof routes_name

  const choiceRouter = (choice: RouteChoices) => {
    if (choice in routes_name) {
      navigate(`/${routes_name[choice]}`)
    } else {
      console.error(`Invalid route choice: ${choice}`)
    }
  }

  return (
    <div className="flex flex-col items-center justify-center flex-1 bg-gray-100 gap-4">
        <Button text="Partida" onClick={() => choiceRouter("partida")} />
        <Button text="Regras" onClick={() => choiceRouter("regras")} />
        <Button text="Voltar para Tela de Login" onClick={() => choiceRouter("login")} />
    </div>
  )
}

export default Home