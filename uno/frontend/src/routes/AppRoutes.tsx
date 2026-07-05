import { createHashRouter } from 'react-router'
import routes_name from './routes'

import App from '../App'
import Home from '../pages/Home'
import Regras from '../pages/Regras'
import Login from '../pages/Login'
import Partida from '../pages/Partida'

const router = createHashRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <Login /> },
      { path: routes_name.regras, element: <Regras /> },
      { path: routes_name.home, element: <Home /> },
      { path: routes_name.partida, element: <Partida />},
    ],
  },
])

export default router