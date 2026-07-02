import { Link } from 'react-router'

function App() {
  return (
    <div>
      <nav>
        <Link to="/">Início</Link> | <Link to="/sobre">Sobre</Link>
      </nav>
    </div>
  )
}

export default App