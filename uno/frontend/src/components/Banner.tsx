import { useNavigate, useLocation, type NavigateFunction } from "react-router";
import routes_name from "../routes/routes";

interface homeHandlerProps {
  current_location: string
  navigate: NavigateFunction
}

function homeHandler({ current_location, navigate }: homeHandlerProps) {
  if (current_location === routes_name.partida) {
    const confirmar = window.confirm("Sair da partida?")
    if (!confirmar) return
  }
  navigate(routes_name.home)
}

function Banner() {
  const navigate = useNavigate()
  const location = useLocation()

  return (
    <div className="flex items-center justify-start gap-3 px-6 py-3 bg-primary shadow-sm">
      <img src="/logo.png" alt="Logo" className="h-20 w-auto" />
      <span
        className="text-6xl font-bold tracking-wide text-white cursor-pointer"
        onClick={() => homeHandler({ current_location: location.pathname, navigate })}
      >
        KUBUNO
      </span>
    </div>
  )
}

export default Banner